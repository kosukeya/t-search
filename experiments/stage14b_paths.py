from t_search.stage14_paths import stage14b_diagnostics


if __name__ == "__main__":
    diagnostics = stage14b_diagnostics()
    for field in diagnostics.__dataclass_fields__:
        print(f"{field}: {getattr(diagnostics, field)}")
