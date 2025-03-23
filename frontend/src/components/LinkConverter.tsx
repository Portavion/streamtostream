import type React from "react";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Clipboard, ClipboardCheck, Loader2 } from "lucide-react";

export default function LinkConverter() {
  const [inputLink, setInputLink] = useState("");
  const [convertedLink, setConvertedLink] = useState("");
  const [isConverting, setIsConverting] = useState(false);
  const [isCopied, setIsCopied] = useState(false);

  const convertLink = async (link: string) => {
    setIsConverting(true);

    const encodedLink = link
      .replaceAll(":", "%3A")
      .replaceAll("/", "%2F")
      .replaceAll("=", "%3D");
    const url = `http://127.0.0.1:8000/api/v1/convert-link/${encodedLink}`;
    let convertedLinks: { links: [string] } = { links: [""] };

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }

      convertedLinks = (await response.json()) as { links: [string] };
      if (!convertedLinks) {
        console.log("error fetching links");
        return;
      }
    } catch (error) {
      console.error(error);
    }

    setConvertedLink(convertedLinks.links[0]);
    setIsConverting(false);
    return convertedLink;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputLink.trim()) {
      console.log("error please enter a streaming link");
      return;
    }
    convertLink(inputLink);
    // setConvertedLink(await convertLink(inputLink));
  };

  const handlePaste = async () => {
    try {
      const text = await navigator.clipboard.readText();
      setInputLink(text);
    } catch (err) {
      console.log("failed to read from clipboard");
      console.log(err);
    }
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(convertedLink);
      setIsCopied(true);

      // Reset the copied state after 2 seconds
      setTimeout(() => {
        setIsCopied(false);
      }, 2000);
    } catch (err) {
      console.log("failed to copy to clipboard");
      console.log(err);
    }
  };

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex flex-col items-center">
          <div className="space-y-2">
            <label htmlFor="streaming-link" className="text-sm font-medium">
              Enter Link:
            </label>
            <div className="flex gap-2 mt-1">
              <Input
                id="streaming-link"
                value={inputLink}
                onChange={(e) => setInputLink(e.target.value)}
                placeholder="https://stream.example.com/watch?v=123"
                className="flex-1"
              />
              <Button
                type="button"
                variant="outline"
                onClick={handlePaste}
                title="Paste from clipboard"
              >
                <Clipboard className="h-4 w-4" />
              </Button>
            </div>
          </div>

          <Button
            type="submit"
            className="w-3/4 border border-green-800 mt-4 hover:bg-green-900"
            disabled={isConverting || !inputLink.trim()}
          >
            {isConverting ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Converting...
              </>
            ) : (
              "Convert Link"
            )}
          </Button>
        </div>
      </form>

      {convertedLink && (
        <div className="space-y-2 p-4 border rounded-md bg-muted/50">
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-medium">Converted Link:</h3>
            <Button
              size="sm"
              variant="ghost"
              onClick={handleCopy}
              className="h-8"
            >
              {isCopied ? (
                <ClipboardCheck className="h-4 w-4 text-green-500" />
              ) : (
                <Clipboard className="h-4 w-4" />
              )}
            </Button>
          </div>
          <div className="p-2 bg-background rounded border break-all text-sm">
            {convertedLink}
          </div>
        </div>
      )}
    </div>
  );
}
