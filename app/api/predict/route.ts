// app/api/predict/route.ts
import { NextResponse } from "next/server"

const API_BASE_URL = process.env.API_BASE_URL

export async function POST(req: Request) {
  if (!API_BASE_URL) {
    return NextResponse.json(
      { error: "API_BASE_URL is not configured on the server" },
      { status: 500 }
    )
  }

  try {
    const body = (await req.json()) as { text?: string }

    if (!body?.text || typeof body.text !== "string") {
      return NextResponse.json(
        { error: "Missing or invalid 'text' field" },
        { status: 400 }
      )
    }

    const upstreamRes = await fetch(`${API_BASE_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: body.text }),
    })

    const data = await upstreamRes.json()

    if (!upstreamRes.ok) {
      return NextResponse.json(
        { error: "Upstream API error", details: data },
        { status: upstreamRes.status }
      )
    }

    // Forward FastAPI response to the client
    return NextResponse.json(data, { status: 200 })
  } catch (err) {
    console.error("Error in /api/predict:", err)
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}
