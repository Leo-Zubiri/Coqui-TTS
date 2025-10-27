from src.test import models_to_test,test_model

def main():
    for lang, models in models_to_test.items():
        for model in models:
            test_model(model, lang)

if __name__ == "__main__":
    main()
