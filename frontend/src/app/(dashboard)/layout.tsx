export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <header className="bg-gray-100 border-b border-gray-200 px-6 py-4">
        <h1 className="text-lg font-semibold">Expense Tracker — DEBUG 1</h1>
      </header>
      {children}
    </div>
  );
}
