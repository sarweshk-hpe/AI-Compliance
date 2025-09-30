import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import './App.css';

// Components
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Evaluate from './pages/Evaluate';
import Audit from './pages/Audit';
import Policies from './pages/Policies';
import Demo from './pages/Demo';

// Create a client
const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="App">
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/evaluate" element={<Evaluate />} />
              <Route path="/audit" element={<Audit />} />
              <Route path="/policies" element={<Policies />} />
              <Route path="/demo" element={<Demo />} />
            </Routes>
          </Layout>
          <Toaster position="top-right" />
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
