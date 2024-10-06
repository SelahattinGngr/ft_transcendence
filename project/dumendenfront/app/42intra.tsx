type Props = {
  code: string;
};

export async function Intra({ code }: Props) {
  const response = await fetch(
    `http://localhost:8000/auth/intra-callback/?code=${code}`,
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
