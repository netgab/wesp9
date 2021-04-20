# wesp9 development

**VS code**

Because of the project folder structure, pylance is not able find the project Python packages (`wesp9/wesp9Lib` is not in the search path).

This is just a cosmetic issue, because Python itself has the folder of the `wesp9.py` file in the search path for modules.

To fix this, create the file `.vscode/settings.json` in the project root with the following content:

```json
{
    "python.analysis.extraPaths": ["./wesp9"]
}
```