from utils import load_vectorstore
from dotenv import load_dotenv
load_dotenv()

vectorstore = load_vectorstore(vectorstore_path="./shopify_vectorstore", index_name="products")
result = vectorstore.similarity_search("I want a adidas shoe for my child")

for product in result:
    print(product.page_content)
    print(product.metadata["images_list"])