type Props = {
  params: {
    token: string;
  };
};

export default async function Profile({ params: { token } }: Props) {
  const response = await fetch("https://api.intra.42.fr/v2/me", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  const json = await response.json();
  return (
    <>
      <pre>
        {token}
        <br />
        {JSON.stringify(json, null, 2)}
      </pre>
    </>
  );
}
