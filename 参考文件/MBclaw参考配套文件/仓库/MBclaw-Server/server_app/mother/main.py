from mbclaw import MBclaw


def main():
    system = MBclaw()

    result = system.run(
        goal="fix bug in authentication module",
        context={
            "env": "dev",
            "priority": "high"
        }
    )

    print("\n=== MBCLAW RESULT ===")
    print(result)


if __name__ == "__main__":
    main()
