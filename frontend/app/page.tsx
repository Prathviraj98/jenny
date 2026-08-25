"use client";

import { useState } from "react";
import { useMcpTools } from "@/lib/api";

export default function HomePage() {
  const [query, setQuery] = useState("");
  const [taskMode, setTaskMode] = useState("quick");
  const [responseText, setResponseText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [hybridScores, setHybridScores] = useState<any>(null);

  const { tools } = useMcpTools();

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    setResponseText("");
    setHybridScores(null);

    const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND || "http://localhost:8000";

    // Fetch Hybrid BM25 + Dense RRF Scores
    try {
      const scoreRes = await fetch(`${BACKEND_URL}/api/v1/search/hybrid-scores`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, task_mode: taskMode })
      });
      if (scoreRes.ok) {
        const scores = await scoreRes.json();
        setHybridScores(scores);
      }
    } catch (err) {
      console.warn("Hybrid scores warning:", err);
    }

    // Stream Token Output via FastAPI Server-Sent Events (SSE) Endpoint
    try {
      const response = await fetch(`${BACKEND_URL}/api/v1/search/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, task_mode: taskMode })
      });

      if (!response.ok || !response.body) {
        throw new Error(`HTTP Error ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          const trimmed = line.trim();
          if (trimmed.startsWith("data: ") && trimmed !== "data: [DONE]") {
            try {
              const parsed = JSON.parse(trimmed.substring(6));
              const delta = parsed.choices?.[0]?.delta?.content || "";
              setResponseText((prev) => prev + delta);
            } catch (e) {}
          }
        }
      }
    } catch (err: any) {
      setResponseText(`[FastAPI Backend Error]: ${err.message || "Failed to connect to backend"}`);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main class="flex-grow flex flex-col items-center justify-start max-w-5xl w-full mx-auto px-4 py-8">
      {/* Header Bar */}
      <div class="w-full flex items-center justify-between py-2 mb-8">
        <div class="flex items-center space-x-2">
          <i class="fas fa-microchip text-brand-400 text-2xl"></i>
          <span class="text-xl font-bold tracking-tight text-white">Nexus AI Engine</span>
          <span class="text-xs px-2 py-0.5 rounded bg-brand-900/60 text-brand-300 font-mono">Next.js 14 + FastAPI</span>
        </div>
        <div class="flex items-center space-x-2 overflow-x-auto no-scrollbar">
          <span class="text-xs text-emerald-400 font-mono flex items-center space-x-1">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>FastAPI Backend Active</span>
          </span>
        </div>
      </div>

      {/* Hero Greeting */}
      <div class="text-center mb-8">
        <h1 class="text-4xl sm:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400 tracking-tight pb-2">
          Enterprise Generative Search
        </h1>
        <p class="text-sm sm:text-base text-gray-400">
          Powered by Next.js 14 App Router, FastAPI 0.110 Async Workers, Redis Caching & Secured API Keys
        </p>
      </div>

      {/* Task Mode Pills */}
      <div class="w-full max-w-2xl mb-4 flex items-center justify-center overflow-x-auto no-scrollbar py-1">
        <div class="inline-flex p-1 rounded-xl glass-panel space-x-1 text-xs">
          {[
            { id: "quick", label: "Quick Answer", icon: "fa-bolt text-yellow-300" },
            { id: "deep", label: "Deep Synthesis", icon: "fa-microscope text-indigo-400" },
            { id: "code", label: "Code Assistant", icon: "fa-code text-emerald-400" },
            { id: "eli5", label: "Explain Simply", icon: "fa-baby text-pink-400" }
          ].map((mode) => (
            <button
              key={mode.id}
              type="button"
              onClick={() => setTaskMode(mode.id)}
              class={`px-3 py-1.5 rounded-lg font-medium transition flex items-center space-x-1.5 ${
                taskMode === mode.id
                  ? "bg-brand-600 text-white shadow"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              <i class={`fas ${mode.icon}`}></i>
              <span>{mode.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Search Input Box */}
      <form onSubmit={handleSearch} class="w-full max-w-2xl relative mb-6">
        <div class="glass-panel rounded-2xl p-2.5 shadow-2xl border border-gray-700/60 focus-within:border-brand-500 flex items-center space-x-2">
          <i class="fas fa-search text-gray-400 ml-2"></i>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask AI or query hybrid search..."
            class="flex-grow bg-transparent outline-none text-white placeholder-gray-400 text-sm px-2"
          />
          <button
            type="submit"
            disabled={isLoading}
            class="px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold transition disabled:opacity-50"
          >
            {isLoading ? "Synthesizing..." : "Search"}
          </button>
        </div>
      </form>

      {/* Hybrid Retrieval Breakdown Bar */}
      {hybridScores && (
        <div class="w-full max-w-2xl p-3 mb-4 rounded-xl glass-panel border border-indigo-500/30 text-xs font-mono text-gray-300 flex flex-wrap items-center justify-between gap-2">
          <span class="text-indigo-400 font-bold"><i class="fas fa-layer-group mr-1"></i>FastAPI Hybrid RAG:</span>
          <span>BM25: <strong class="text-white">{hybridScores.bm25_score}</strong></span>
          <span>Bi-Encoder: <strong class="text-white">{hybridScores.dense_score}</strong></span>
          <span>RRF Rank: <strong class="text-white">{hybridScores.rrf_rank}</strong></span>
          <span>Cross-Encoder: <strong class="text-emerald-400">{hybridScores.cross_encoder_score}</strong></span>
        </div>
      )}

      {/* Response Box */}
      {responseText && (
        <div class="w-full max-w-2xl glass-panel rounded-2xl border border-gray-700 overflow-hidden shadow-2xl p-6 mb-8 text-sm text-gray-200 leading-relaxed space-y-3">
          <div class="flex items-center justify-between border-b border-gray-800 pb-3 text-xs">
            <span class="font-bold text-brand-400 flex items-center space-x-1.5">
              <i class="fas fa-robot"></i>
              <span>AI Search Response (Streamed via FastAPI)</span>
            </span>
            <span class="text-gray-500 font-mono">Secured Server API Keys</span>
          </div>
          <div class="whitespace-pre-wrap">{responseText}</div>
        </div>
      )}

      {/* MCP Tools Inspector Overview */}
      <div class="w-full max-w-2xl p-4 rounded-2xl glass-panel border border-gray-800 text-xs space-y-2">
        <h3 class="font-bold text-teal-300 flex items-center space-x-2">
          <i class="fas fa-network-wired"></i>
          <span>Active MCP Tools (FastAPI Microservice)</span>
        </h3>
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 font-mono text-[11px]">
          {tools.map((t: any) => (
            <div key={t.name} class="p-2 bg-gray-950 rounded border border-gray-800 flex items-center justify-between">
              <span>{t.name}</span>
              <span class="text-emerald-400">online</span>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
