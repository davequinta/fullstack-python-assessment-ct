"use client";

import { useEffect, useState } from "react";
import axios from "axios";

export default function Home() {
  const [orderStatus, setOrderStatus] = useState("Loading order status...");

  useEffect(() => {
    // Fetch the initial order status
    const fetchOrderStatus = async () => {
      try {
        const response = await axios.get("http://localhost:8000/orders/3");
        setOrderStatus(`Order ${response.data.id} status: ${response.data.status}`);
      } catch (error) {
        console.error("Error fetching order status:", error);
        setOrderStatus("Error loading order status");
      }
    };

    fetchOrderStatus();

    // Set up WebSocket connection
    const websocket = new WebSocket("ws://localhost:8000/ws/orders/3");

    websocket.onopen = () => {
      console.log("WebSocket connection opened");
    };

    websocket.onmessage = (event) => {
      console.log("WebSocket message received:", event.data);
      try {
        const data = JSON.parse(event.data);
        console.log("Parsed data:", data);
        setOrderStatus(`Order ${data.order_id} status: ${data.status}`);
      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    };

    websocket.onclose = () => {
      console.log("WebSocket connection closed");
    };

    websocket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    const keepAlive = setInterval(() => {
      if (websocket.readyState === WebSocket.OPEN) {
        console.log("Sending keep-alive message");
        websocket.send(JSON.stringify({ type: "keep-alive" }));
      }
    }, 30000);

    return () => {
      clearInterval(keepAlive);
      websocket.close();
    };
  }, []);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8 sm:p-20 bg-gradient-to-r from-blue-500 to-purple-600 text-white">
      <header className="mb-8">
        <h1 className="text-4xl font-bold">Order Tracking</h1>
      </header>
      <main className="flex flex-col items-center bg-white p-8 rounded-lg shadow-lg text-gray-800">
        <h1 className="text-3xl font-bold mb-4">Real-time Order Status</h1>
        <p className="text-lg">{orderStatus}</p>
      </main>
      <footer className="mt-8 flex gap-6 flex-wrap items-center justify-center">
        <a
          href="https://davidquinta.tech/"
          target="_blank"
          rel="noopener noreferrer"
          className="underline"
        >
          Created by David Q.
        </a>
      </footer>
    </div>
  );
}
