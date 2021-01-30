import runpy


def main():
    app_package = runpy.run_module(
        mod_name="src.githubsecrets", init_globals=globals())
    app_package['main']()


if __name__ == "__main__":
    main()
