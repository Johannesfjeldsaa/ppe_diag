from ppe_diag.scripts.main.config import main_config

def main():
    config = main_config.from_cli()
    config.setup_logging()

    checked_config = config.get_checked_and_derived_config()

    # continue with the rest of the main logic

if __name__ == "__main__":
    main()