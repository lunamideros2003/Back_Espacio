import app.main as main_module


def test_init_database_skips_when_disabled(monkeypatch):
    calls = []
    monkeypatch.setattr(main_module.settings, "auto_create_tables", False)
    monkeypatch.setattr(main_module, "ensure_schema", lambda: calls.append("schema"))
    monkeypatch.setattr(main_module.Base.metadata, "create_all", lambda **_kwargs: calls.append("tables"))
    monkeypatch.setattr(main_module, "seed_if_empty", lambda: calls.append("seed"))

    main_module.init_database()

    assert calls == []
