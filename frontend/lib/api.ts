import axios from 'axios';
import useSWR from 'swr';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: `${BACKEND_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetcher = (url: string) => apiClient.get(url).then((res) => res.data);

export function useMcpTools() {
  const { data, error, isLoading } = useSWR('/mcp/tools', fetcher, {
    revalidateOnFocus: false,
  });
  return {
    tools: data?.result?.tools || [],
    resources: data?.result?.resources || [],
    prompts: data?.result?.prompts || [],
    isLoading,
    isError: error,
  };
}

export function useUserProfile() {
  const { data, error, isLoading } = useSWR('/users/me', fetcher);
  return {
    user: data,
    isLoading,
    isError: error,
  };
}
