import Link from "next/link";
import { Intra } from "./42intra";
import { Button } from "@/components/ui/button";

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
        <>
          <Button>
            <Link href={data.data.url}>Login with Intra</Link>
          </Button>
          <Button>
            <Link href="/auth/signup">Signup</Link>
          </Button>
        </>
      )}
    </div>
  );
}
