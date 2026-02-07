def test_import_package():
    import quantumpytho

    assert hasattr(quantumpytho, "__version__")


def test_menu_entrypoint():
    from quantumpytho import menu

    assert callable(menu.run_app)
