# Написать программу, которая скачивает изображения с заданных URL-адресов и 
# сохраняет их на диск. Каждое изображение должно сохраняться в отдельном файле, название 
# которого соответствует названию изображения в URL-адресе.
# Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
# — Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
# — Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
# — Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения программы.

import asyncio
import aiohttp
import time
import os

urls = ['https://www.xtrafondos.com/thumbs/vertical/1_4321.jpg',
        'https://m.media-amazon.com/images/I/A11iNMo6fnL._SL1500_.jpg',
        'https://i.pinimg.com/564x/4f/20/c3/4f20c3e7cc2116484670da31087ed1ba.jpg',
        'https://www.candb.com/site/candb/images/artwork/Dark-Souls-Artorias-of-the-Abyss_Nekro-Bandai-1600.jpg',
        'https://hips.hearstapps.com/hmg-prod/images/flower-meanings-1671510935.jpg', ]

async def download(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    filename = 'asyncio_' + os.path.basename(url)
                    with open(os.path.join('flaskk/f4/f4_images_asyncio/', filename), "wb") as f:
                        total, size = (0, 4092)
                        res = response.content.iter_chunked(size)
                        start_time = time.time()
                        async for chunk in res:
                            f.write(chunk)
                            total += size
                            print(f"Downloaded {url}: {total / 1024:.2f} kB in {time.time() - start_time:.2f} seconds")
                else:
                    print(f"Failed to download {url}: Status {response.status}")
        except Exception as e:
            print(f"Error downloading {url}: {str(e)}")

async def main():
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    if not os.path.exists('flaskk/f4/f4_images_asyncio/'):
        os.makedirs('flaskk/f4/f4_images_asyncio/')
    
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print(f"Total execution time: {time.time() - start_time:.2f} seconds")
