LANGUAGES = {
    "python": {
        "extension": ".py",
        "docker_image": "runner-python",
        "compile": None,
        "run": ["python3", "/code.py"]
    },
    "java": {
        "extension": ".java",
        "docker_image": "runner-java",
        "compile": ["javac", "Solver.java"],
        "run": ["java", "Solver"]

    },
    "csharp": {
        "extension": ".cs",
        "docker_image": "runner-csharp",
        "compile": ["mcs", "-out:Program.exe", "Program.cs"],
        "run": ["mono", "Program.exe"]
    }
}
