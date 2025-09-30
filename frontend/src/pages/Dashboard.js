import React from 'react';
import { useQuery } from 'react-query';
import { Shield, AlertTriangle, CheckCircle, Clock, TrendingUp } from 'lucide-react';
import axios from 'axios';

const Dashboard = () => {
  const { data: stats, isLoading, error } = useQuery('systemStats', async () => {
    const response = await axios.get('/api/v1/admin/stats');
    return response.data;
  });

  const { data: recentEvents, isLoading: eventsLoading } = useQuery('recentEvents', async () => {
    const response = await axios.get('/api/v1/audit/events?limit=5');
    return response.data;
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="actum-text-muted">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="hpe-text-error">
        Error loading dashboard: {error.message}
      </div>
    );
  }

  const getDecisionColor = (decision) => {
    switch (decision) {
      case 'block':
        return 'actum-badge-danger';
      case 'flag':
        return 'actum-badge-warning';
      case 'allow':
        return 'actum-badge-success';
      default:
        return 'actum-badge-info';
    }
  };

  const getRiskLevelColor = (riskLevel) => {
    switch (riskLevel) {
      case 'unacceptable':
        return 'actum-badge-danger';
      case 'high':
        return 'actum-badge-warning';
      case 'limited':
        return 'actum-badge-info';
      case 'minimal':
        return 'actum-badge-success';
      default:
        return 'actum-badge-info';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold actum-text-primary">Dashboard</h1>
        <p className="actum-text-secondary">AI Compliance Overview</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="actum-card-stats">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Shield className="h-8 w-8 text-hpe-core-blue" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium actum-text-muted">Total Events</p>
              <p className="text-2xl font-semibold actum-text-primary">
                {stats?.audit_events?.total || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="actum-card-stats">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <AlertTriangle className="h-8 w-8 text-hpe-status-light-critical" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium actum-text-muted">Blocked</p>
              <p className="text-2xl font-semibold actum-text-primary">
                {stats?.audit_events?.blocked || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="actum-card-stats">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Clock className="h-8 w-8 text-hpe-status-light-warning" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium actum-text-muted">Flagged</p>
              <p className="text-2xl font-semibold actum-text-primary">
                {stats?.audit_events?.flagged || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="actum-card-stats">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <CheckCircle className="h-8 w-8 text-hpe-status-light-ok" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium actum-text-muted">Allowed</p>
              <p className="text-2xl font-semibold actum-text-primary">
                {stats?.audit_events?.allowed || 0}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Events */}
      <div className="actum-card-elevated">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold actum-text-primary">Recent Events</h2>
          <TrendingUp className="h-5 w-5 actum-text-muted" />
        </div>
        
        {eventsLoading ? (
          <div className="actum-text-muted">Loading recent events...</div>
        ) : (
          <div className="space-y-4">
            {recentEvents?.map((event) => (
              <div key={event.event_id} className="actum-border-b pb-4 last:border-b-0">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <span className={`actum-badge-modern ${getDecisionColor(event.decision)}`}>
                        {event.decision.toUpperCase()}
                      </span>
                      <span className={`actum-badge-modern ${getRiskLevelColor(event.risk_level)}`}>
                        {event.risk_level}
                      </span>
                    </div>
                    <p className="text-sm actum-text-secondary mt-1">{event.explanation}</p>
                    <p className="text-xs actum-text-muted mt-1">
                      {event.user} • {new Date(event.timestamp).toLocaleString()}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium actum-text-primary">{event.event_id}</p>
                    <p className="text-xs actum-text-muted">Confidence: {event.confidence_score}%</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Policy Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="actum-card-gradient">
          <h2 className="text-lg font-semibold actum-text-primary mb-4">Policy Overview</h2>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-sm actum-text-secondary">Active Policy Packs</span>
              <span className="text-sm font-medium actum-text-primary">{stats?.policies?.active_packs || 0}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm actum-text-secondary">Total Policy Tags</span>
              <span className="text-sm font-medium actum-text-primary">{stats?.policies?.total_tags || 0}</span>
            </div>
          </div>
        </div>

        <div className="actum-card-accent">
          <h2 className="text-lg font-semibold actum-text-primary mb-4">Compliance Status</h2>
          <div className="space-y-3">
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 text-hpe-status-light-ok mr-2" />
              <span className="text-sm actum-text-secondary">AI Compliance Active</span>
            </div>
            <div className="flex items-center">
              <Shield className="h-5 w-5 text-hpe-core-blue mr-2" />
              <span className="text-sm actum-text-secondary">Audit Trail Immutable</span>
            </div>
            <div className="flex items-center">
              <AlertTriangle className="h-5 w-5 text-hpe-status-light-warning mr-2" />
              <span className="text-sm actum-text-secondary">Real-time Monitoring</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
