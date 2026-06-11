from eda_automation import generate_daily_eda_report


def run_daily_pipeline():

    print("\n=== MARKETMIND DAILY PIPELINE ===")

    print("\nRunning EDA...")
    generate_daily_eda_report()

    print("✓ EDA completed")

    print("\nPipeline finished successfully.")


if __name__ == "__main__":
    run_daily_pipeline()