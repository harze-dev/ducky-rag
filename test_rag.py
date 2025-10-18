import asyncio, json, os, sys

# Ensure project root is in path
sys.path.append(os.getcwd())

from services.rag import ask_book

async def main():
    result = await ask_book("What is the main idea of the book?", return_image=False)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
