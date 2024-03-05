"use client";
import React, { useEffect, useState } from "react";
import dynamic from "next/dynamic";

// load PDF2TriplesPage only on client side, so use dynamic import
const DynamicPDF2TriplesPage = dynamic(
  () => import("features/pdf2triples/PDF2TriplesPage"),
  { ssr: false },
);

export default function PDF2Triples() {
  // Make sure store was initialized before rendering the page to avoid hydration errors
  const [initialized, setInitialized] = useState(false);
  useEffect(() => {
    setInitialized(true);
  }, []);
  if (!initialized) return <></>;

  return <DynamicPDF2TriplesPage />;
}
