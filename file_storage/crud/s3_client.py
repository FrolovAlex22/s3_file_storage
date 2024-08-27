import asyncio
from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from botocore.exceptions import ClientError


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config, verify=False) as client:
            yield client

    async def upload_file(
            self,
            file_path: str,
            name: str
    ):
        try:
            async with self.get_client() as client:
                with open(file_path, "rb") as file:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=name,
                        Body=file
                    )
                print(f"File {name} uploaded to {self.bucket_name}")
        except ClientError as e:
            print(f"Error uploading file: {e}")

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                print(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            print(f"Error deleting file: {e}")

    async def get_file(self, object_name: str, destination_path: str):
        try:
            async with self.get_client() as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
                data = await response["Body"].read()
                with open(destination_path, "wb") as file:
                    file.write(data)
                print(f"File {object_name} downloaded to {destination_path}")
                return file
        except ClientError as e:
            print(f"Error downloading file: {e}")


async def encoding_s3_name(user_id: int, file_name: str) -> str:
    return f"{user_id}#{file_name}"


async def decoding_s3_name(s3_name: str) -> str:
    return s3_name.split("#")[-1]

# async def main():
#     s3_client = S3Client(
#         access_key="8a1a156ae5f0447ab01cd4191d744b90",
#         secret_key="5c622c0ddd7e4a7aa2933aa1909a3191",
#         endpoint_url="https://s3.storage.selcloud.ru",  # для Selectel используйте https://s3.storage.selcloud.ru
#         bucket_name="5d-test",
#     )

#     # Проверка, что мы можем загрузить, скачать и удалить файл
#     await s3_client.upload_file("test.jpg")
#     # await s3_client.get_file("test.jpg", "test_local_file.jpg")
#     # await s3_client.delete_file("test.jpg")


# if __name__ == "__main__":
#     asyncio.run(main())
