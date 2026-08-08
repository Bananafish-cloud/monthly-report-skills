# -*- coding: utf-8 -*-
"""环境检测脚本 — 月报自动化前置检查。

用法: python check_env.py
通过: 所有 [OK]  失败: 打印 [FAIL] + 修复指引, exit 1
"""
import sys, os, subprocess

def main():
    problems = []
    checks = []

    # 1. Windows
    checks.append(("操作系统", sys.platform == "win32",
                   f"当前 {sys.platform}，COM 方案仅限 Windows"))
    # 2. PowerPoint COM
    try:
        import win32com.client
        app = win32com.client.Dispatch("PowerPoint.Application")
        app.Quit()
        checks.append(("PowerPoint COM", True, ""))
    except Exception as e:
        checks.append(("PowerPoint COM", False,
                       f"无法启动 PowerPoint COM（{e}）。请确认已安装 Microsoft PowerPoint（不是 WPS）。"))
    # 3. Python 版本
    py_ok = sys.version_info >= (3, 9)
    checks.append(("Python >= 3.9", py_ok, f"当前 {sys.version}"))
    # 4. pywin32
    try:
        import win32com  # noqa
        checks.append(("pywin32", True, ""))
    except ImportError:
        checks.append(("pywin32", False, "pip install pywin32"))

    # 5. 模板文件（从参数或 answers.json 读）
    template = None
    if len(sys.argv) > 1:
        template = sys.argv[1]
    elif os.path.exists("answers.json"):
        import json
        try:
            template = json.load(open("answers.json", encoding="utf-8")).get("template_path")
        except Exception:
            pass
    if template:
        checks.append(("模板文件", os.path.isfile(template) and template.endswith(".pptx"),
                       f"{template}"))

    all_ok = True
    for name, ok, msg in checks:
        status = "[OK]  " if ok else "[FAIL]"
        print(f"{status} {name}" + (f"  - {msg}" if msg and not ok else ""))
        if not ok:
            all_ok = False
            if msg:
                problems.append(msg)
    print("=" * 40)
    if all_ok:
        print("环境检查全部通过")
        return 0
    print("环境检查失败，请先修复：")
    for p in problems:
        print(f"  - {p}")
    return 1

if __name__ == "__main__":
    sys.exit(main())
