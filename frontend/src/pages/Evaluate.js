import React, { useState } from 'react';
import { useMutation } from 'react-query';
import { Send, Upload, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const Evaluate = () => {
  const [formData, setFormData] = useState({
    client_id: 'demo-client',
    user: 'demo-user',
    input_type: 'text',
    input: ''
  });
  const [selectedFile, setSelectedFile] = useState(null);

  const evaluateMutation = useMutation(
    async (data) => {
      if (selectedFile) {
        // Use form data for file upload
        const formDataToSend = new FormData();
        formDataToSend.append('text', data.input);
        formDataToSend.append('client_id', data.client_id);
        formDataToSend.append('user', data.user);
        formDataToSend.append('input_type', 'text_with_image');
        formDataToSend.append('image', selectedFile);
        
        const response = await axios.post('/api/v1/evaluate/with-image', formDataToSend);
        return response.data;
      } else {
        // Use JSON for text-only
        const response = await axios.post('/api/v1/evaluate/', data);
        return response.data;
      }
    },
    {
      onSuccess: (data) => {
        toast.success('Content evaluated successfully!');
      },
      onError: (error) => {
        toast.error(`Evaluation failed: ${error.response?.data?.detail || error.message}`);
      }
    }
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.input.trim()) {
      toast.error('Please enter some content to evaluate');
      return;
    }
    evaluateMutation.mutate(formData);
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
    } else {
      toast.error('Please select a valid image file');
    }
  };

  const getDecisionIcon = (decision) => {
    switch (decision) {
      case 'block':
        return <XCircle className="h-6 w-6 text-red-600" />;
      case 'flag':
        return <AlertTriangle className="h-6 w-6 text-yellow-600" />;
      case 'allow':
        return <CheckCircle className="h-6 w-6 text-green-600" />;
      default:
        return null;
    }
  };

  const getDecisionColor = (decision) => {
    switch (decision) {
      case 'block':
        return 'bg-red-50';
      case 'flag':
        return 'bg-yellow-50';
      case 'allow':
        return 'bg-green-50';
      default:
        return 'bg-gray-50';
    }
  };

  const sampleInputs = [
    {
      label: 'Biometric Intent',
      text: 'We will scrape faces from social media to build a facial recognition database',
      description: 'Should trigger ProhibitedBiometric policy'
    },
    {
      label: 'High-Risk AI',
      text: 'AI-powered CV screening system for recruitment',
      description: 'Should trigger HighRiskAI policy'
    },
    {
      label: 'Limited Risk',
      text: 'Chatbot for customer service',
      description: 'Should trigger LimitedRiskAI policy'
    },
    {
      label: 'Safe Content',
      text: 'Weather forecast for tomorrow',
      description: 'Should be allowed'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Content Evaluation</h1>
        <p className="text-gray-600">Test EU AI Act compliance policies against your content</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <div className="actum-card-elevated">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Evaluate Content</h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Content to Evaluate
              </label>
              <textarea
                value={formData.input}
                onChange={(e) => setFormData({ ...formData, input: e.target.value })}
                className="actum-input h-32 resize-none"
                placeholder="Enter text content to evaluate against EU AI Act compliance policies..."
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Upload Image (Optional)
              </label>
              <div className="flex items-center space-x-2">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileChange}
                  className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                />
                {selectedFile && (
                  <button
                    type="button"
                    onClick={() => setSelectedFile(null)}
                    className="text-red-600 hover:text-red-800"
                  >
                    <XCircle className="h-5 w-5" />
                  </button>
                )}
              </div>
              {selectedFile && (
                <p className="text-sm text-gray-500 mt-1">
                  Selected: {selectedFile.name}
                </p>
              )}
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Client ID
                </label>
                <input
                  type="text"
                  value={formData.client_id}
                  onChange={(e) => setFormData({ ...formData, client_id: e.target.value })}
                  className="actum-input"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  User
                </label>
                <input
                  type="text"
                  value={formData.user}
                  onChange={(e) => setFormData({ ...formData, user: e.target.value })}
                  className="actum-input"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={evaluateMutation.isLoading}
              className="actum-button-primary w-full flex items-center justify-center"
            >
              {evaluateMutation.isLoading ? (
                'Evaluating...'
              ) : (
                <>
                  <Send className="h-4 w-4 mr-2" />
                  Evaluate Content
                </>
              )}
            </button>
          </form>
        </div>

        {/* Sample Inputs */}
        <div className="actum-card-gradient">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Sample Inputs</h2>
          <div className="space-y-3">
            {sampleInputs.map((sample, index) => (
              <div key={index} className="actum-card-icon-bg rounded-md p-3">
                <h3 className="font-medium text-gray-900 mb-1">{sample.label}</h3>
                <p className="text-sm text-gray-600 mb-2">{sample.description}</p>
                <button
                  onClick={() => setFormData({ ...formData, input: sample.text })}
                  className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                >
                  Use this example
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Results */}
      {evaluateMutation.data && (
        <div className={`actum-card-accent ${getDecisionColor(evaluateMutation.data.decision)}`}>
          <div className="flex items-start justify-between">
            <div className="flex items-center space-x-3">
              {getDecisionIcon(evaluateMutation.data.decision)}
              <div>
                <h2 className="text-lg font-semibold text-gray-900">
                  Evaluation Result: {evaluateMutation.data.decision.toUpperCase()}
                </h2>
                <p className="text-sm text-gray-600">
                  Risk Level: {evaluateMutation.data.risk_level}
                </p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm font-medium text-gray-900">
                Confidence: {evaluateMutation.data.confidence_score}%
              </p>
              <p className="text-xs text-gray-500">
                Policy: {evaluateMutation.data.policy_version}
              </p>
            </div>
          </div>

          <div className="mt-4">
            <h3 className="font-medium text-gray-900 mb-2">Explanation</h3>
            <p className="text-sm text-gray-600">{evaluateMutation.data.explanation}</p>
          </div>

          {evaluateMutation.data.policy_tags.length > 0 && (
            <div className="mt-4">
              <h3 className="font-medium text-gray-900 mb-2">Triggered Policies</h3>
              <div className="flex flex-wrap gap-2">
                {evaluateMutation.data.policy_tags.map((tag, index) => (
                  <span key={index} className="actum-badge-modern actum-badge-danger">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="mt-4 pt-4 border-t border-gray-200">
            <p className="text-xs text-gray-500">
              Audit Event ID: {evaluateMutation.data.audit_event_id}
            </p>
          </div>
        </div>
      )}

      {/* Error Display */}
      {evaluateMutation.error && (
        <div className="actum-card-glass bg-red-50">
          <div className="flex items-center space-x-2">
            <XCircle className="h-5 w-5 text-red-600" />
            <h3 className="font-medium text-red-900">Evaluation Error</h3>
          </div>
          <p className="text-sm text-red-700 mt-2">
            {evaluateMutation.error.response?.data?.detail || evaluateMutation.error.message}
          </p>
        </div>
      )}
    </div>
  );
};

export default Evaluate;
