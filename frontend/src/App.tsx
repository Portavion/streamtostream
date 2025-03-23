import LinkConverter from "./components/LinkConverter";

export default function Home() {
  return (
    <main className="flex flex-col justify-center items-center  p-4 md:p-24 w-full">
      <div className="max-w-6xl">
        <h1 className="text-3xl font-bold text-center mb-6">
          Stream to Stream
        </h1>
        <LinkConverter />
      </div>
    </main>
  );
}
