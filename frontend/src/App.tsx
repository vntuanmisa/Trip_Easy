import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';

// Import i18n configuration
import './i18n';

// Import pages
import Dashboard from './pages/Dashboard';
import TripDetail from './pages/TripDetail';
import CreateTrip from './pages/CreateTrip';
import JoinTrip from './pages/JoinTrip';
import NotFound from './pages/NotFound';

// Import components
import Layout from './components/Layout';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="App min-h-screen bg-gray-50">
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/trips/create" element={<CreateTrip />} />
              <Route path="/trips/join" element={<JoinTrip />} />
              <Route path="/trips/join/:inviteCode" element={<JoinTrip />} />
              <Route path="/trips/:tripId" element={<TripDetail />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </Layout>
          
          {/* Toast notifications */}
          <Toaster
            position="top-center"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
              success: {
                style: {
                  background: '#10B981',
                },
              },
              error: {
                style: {
                  background: '#EF4444',
                },
              },
            }}
          />
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;