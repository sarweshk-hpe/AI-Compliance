import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { Eye, Download, Filter, Calendar } from 'lucide-react';
import axios from 'axios';

const Audit = () => {
  const [filters, setFilters] = useState({
    decision: '',
    risk_level: '',
    user: '',
    limit: 50
  });

  const { data: events, isLoading, error } = useQuery(
    ['auditEvents', filters],
    async () => {
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });
      const response = await axios.get(`/api/v1/audit/events?${params}`);
      return response.data;
    }
  );

  const getDecisionColor = (decision) => {
    switch (decision) {
      case 'block':
        return 'text-red-600 bg-red-100';
      case 'flag':
        return 'text-yellow-600 bg-yellow-100';
      case 'allow':
        return 'text-green-600 bg-green-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getRiskLevelColor = (riskLevel) => {
    switch (riskLevel) {
      case 'unacceptable':
        return 'text-red-600 bg-red-100';
      case 'high':
        return 'text-orange-600 bg-orange-100';
      case 'limited':
        return 'text-yellow-600 bg-yellow-100';
      case 'minimal':
        return 'text-green-600 bg-green-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const exportAuditBundle = async (eventId) => {
    try {
      const response = await axios.get(`/api/v1/audit/export/${eventId}`);
      const blob = new Blob([JSON.stringify(response.data, null, 2)], {
        type: 'application/json'
      });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `audit-bundle-${eventId}.json`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Export failed:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading audit events...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500">
        Error loading audit events: {error.message}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Audit Trail</h1>
        <p className="text-gray-600">Immutable audit events with HMAC signatures</p>
      </div>

      {/* Filters */}
      <div className="actum-card-elevated">
        <div className="flex items-center space-x-2 mb-4">
          <Filter className="h-5 w-5 text-gray-500" />
          <h2 className="text-lg font-semibold text-gray-900">Filters</h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Decision</label>
            <select
              value={filters.decision}
              onChange={(e) => setFilters({ ...filters, decision: e.target.value })}
              className="actum-input"
            >
              <option value="">All</option>
              <option value="block">Block</option>
              <option value="flag">Flag</option>
              <option value="allow">Allow</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Risk Level</label>
            <select
              value={filters.risk_level}
              onChange={(e) => setFilters({ ...filters, risk_level: e.target.value })}
              className="actum-input"
            >
              <option value="">All</option>
              <option value="unacceptable">Unacceptable</option>
              <option value="high">High</option>
              <option value="limited">Limited</option>
              <option value="minimal">Minimal</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">User</label>
            <input
              type="text"
              value={filters.user}
              onChange={(e) => setFilters({ ...filters, user: e.target.value })}
              className="actum-input"
              placeholder="Filter by user"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Limit</label>
            <select
              value={filters.limit}
              onChange={(e) => setFilters({ ...filters, limit: e.target.value })}
              className="actum-input"
            >
              <option value="10">10</option>
              <option value="25">25</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
          </div>
        </div>
      </div>

      {/* Events Table */}
      <div className="actum-card-table">
        <div className="flex items-center justify-between mb-4 p-6 pb-0">
          <h2 className="text-lg font-semibold text-gray-900">Audit Events</h2>
          <span className="text-sm text-gray-500">
            {events?.length || 0} events found
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Event ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Timestamp
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  User
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Decision
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Risk Level
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Confidence
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {events?.map((event) => (
                <tr key={event.event_id} className="hover:bg-gray-50 transition-colors duration-150">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {event.event_id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(event.timestamp).toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {event.user}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`actum-badge-modern ${getDecisionColor(event.decision)}`}>
                      {event.decision.toUpperCase()}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`actum-badge-modern ${getRiskLevelColor(event.risk_level)}`}>
                      {event.risk_level}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {event.confidence_score}%
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2">
                      <button
                        onClick={() => exportAuditBundle(event.event_id)}
                        className="text-blue-600 hover:text-blue-900 transition-colors duration-150"
                        title="Export audit bundle"
                      >
                        <Download className="h-4 w-4" />
                      </button>
                      <button
                        className="text-gray-600 hover:text-gray-900 transition-colors duration-150"
                        title="View details"
                      >
                        <Eye className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {events?.length === 0 && (
          <div className="text-center py-8">
            <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">No audit events found</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Audit;
