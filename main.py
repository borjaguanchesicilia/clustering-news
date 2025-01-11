from clustering_project.utils.utils import process_headers, load_news


if __name__ == "__main__" :

    news_goldstandard = load_news("./data/gold-standard")

    process_headers(input_directory="./data/gold-standard/",
                    output_directory="./data/output")