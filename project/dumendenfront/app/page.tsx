import Link from "next/Link";
import { Intra } from "./42intra";
type Props = {
  searchParams: { code?: string };
};

export default async function Home({ searchParams }: Props) {
  const response = await fetch("http://apigateway:8000/auth/intra");
  const data = await response.json();

  return (
    <div>
      <pre>{JSON.stringify(data, null, 2)}</pre>
      {searchParams.code ? (
        <Intra code={searchParams.code} />
      ) : (
        <Link href={data.data.url}>Login with Intra</Link>
      )}
    </div>
  );
}
