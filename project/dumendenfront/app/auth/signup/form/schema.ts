import { z } from "zod";

export const signupFormSchema = z.object({
  username: z.string().min(3),
  email: z.string().email(),
  firstName: z.string().min(2),
  lastName: z.string().min(2),
  avatar_url: z.string().default(""),
  password: z.string().min(6),
});

export type SignupFormSchema = z.infer<typeof signupFormSchema>;
