export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 'no-store, max-age=0');
  return res.status(200).json({
    groqKey: process.env.GROQ_API_KEY || '',
    geminiKey: process.env.GEMINI_API_KEY || ''
  });
}
