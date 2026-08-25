import { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import axios from "axios";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND || "http://localhost:8000";

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        username: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        if (!credentials?.username || !credentials?.password) return null;
        try {
          const formData = new URLSearchParams();
          formData.append("username", credentials.username);
          formData.append("password", credentials.password);

          const res = await axios.post(`${BACKEND_URL}/api/v1/auth/login`, formData, {
            headers: { "Content-Type": "application/x-www-form-urlencoded" }
          });

          if (res.data && res.data.access_token) {
            return {
              id: res.data.user_id || "1",
              email: credentials.username,
              accessToken: res.data.access_token,
              refreshToken: res.data.refresh_token
            };
          }
          return null;
        } catch (error) {
          console.error("Auth login error:", error);
          return null;
        }
      }
    })
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.accessToken = (user as any).accessToken;
        token.refreshToken = (user as any).refreshToken;
      }
      return token;
    },
    async session({ session, token }) {
      (session as any).accessToken = token.accessToken;
      return session;
    }
  },
  session: { strategy: "jwt" },
  pages: { signIn: "/" }
};
