type Props = {
  searchParams: { code?: string };
};

export default async function callback({ searchParams: { code } }: Props) {
  const response = await fetch(
    `http://apigateway:8000/auth/intra-callback/?code=${code}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept-Language": "tr",
      },
      body: JSON.stringify({ code }),
    }
  );
  const data = await response.json();
  return (
    <>
      {code}
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </>
  );
}
