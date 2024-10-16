"use server";

import { SignupFormSchema } from "./schema";

export async function signup(data: SignupFormSchema) {
  console.log("signup data", data);
  const request = await fetch("http://apigateway:8000/auth/signup/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept-language": "tr",
    },
    body: JSON.stringify(data),
  });
  const json = await request.json();
  if (!request.ok) {
    return { status: false, message: json.error };
  }

  return { status: true, message: "işlem başarılı kanzi" };
}
