import React from 'react';
import { useQuery } from 'react-query';
import { Shield, Tag, Package } from 'lucide-react';
import axios from 'axios';

const Policies = () => {
  const { data: tags, isLoading: tagsLoading } = useQuery('policyTags', async () => {
    const response = await axios.get('/api/v1/policies/tags');
    return response.data;
  });

  const { data: packs, isLoading: packsLoading } = useQuery('policyPacks', async () => {
    const response = await axios.get('/api/v1/policies/packs');
    return response.data;
  });

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

  const getActionColor = (action) => {
    switch (action) {
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

  if (tagsLoading || packsLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading policies...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Policies</h1>
        <p className="text-gray-600">EU AI Act compliance policy packs and tags</p>
      </div>

      {/* Policy Packs */}
      <div className="actum-card-elevated">
        <div className="flex items-center space-x-2 mb-4">
          <Package className="h-5 w-5 text-gray-500" />
          <h2 className="text-lg font-semibold text-gray-900">Policy Packs</h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {packs?.map((pack) => (
            <div key={pack.id} className="actum-card-gradient rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-medium text-gray-900">{pack.name}</h3>
                <span className={`actum-badge-modern ${
                  pack.is_active ? 'text-green-600 bg-green-100' : 'text-gray-600 bg-gray-100'
                }`}>
                  {pack.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              <p className="text-sm text-gray-600 mb-2">{pack.description}</p>
              <div className="text-xs text-gray-500">
                <p>Version: {pack.version}</p>
                <p>Created: {new Date(pack.created_at).toLocaleDateString()}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Policy Tags */}
      <div className="actum-card-table">
        <div className="flex items-center space-x-2 mb-4 p-6 pb-0">
          <Tag className="h-5 w-5 text-gray-500" />
          <h2 className="text-lg font-semibold text-gray-900">Policy Tags</h2>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tag Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Description
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Risk Level
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Action
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Policy Pack
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {tags?.map((tag) => (
                <tr key={tag.id} className="hover:bg-gray-50 transition-colors duration-150">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {tag.name}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {tag.description}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`actum-badge-modern ${getRiskLevelColor(tag.risk_level)}`}>
                      {tag.risk_level}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`actum-badge-modern ${getActionColor(tag.action)}`}>
                      {tag.action}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {tag.policy_pack}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Policies;
