import React, { useState } from 'react';
import { useMutation } from 'react-query';
import { Play, ArrowRight, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const Demo = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [results, setResults] = useState({});

  const evaluateMutation = useMutation(
    async (data) => {
      const response = await axios.post('/api/v1/evaluate/', data);
      return response.data;
    },
    {
      onSuccess: (data, variables) => {
        setResults(prev => ({ ...prev, [variables.scenario]: data }));
        toast.success(`${variables.scenario} completed!`);
      },
      onError: (error) => {
        toast.error(`Demo failed: ${error.response?.data?.detail || error.message}`);
      }
    }
  );

  const demoScenarios = [
    {
      id: 'biometric',
      title: 'Scenario A: Biometric Intent Detection',
      description: 'Test detection of prohibited biometric identification practices',
      input: {
        client_id: 'demo-client',
        user: 'demo-user',
        input_type: 'text',
        input: 'We will scrape faces from social media to build a facial recognition database for real-time identification'
      },
      expected: {
        decision: 'block',
        policy_tags: ['ProhibitedBiometric'],
        risk_level: 'unacceptable'
      },
      explanation: 'This should trigger the ProhibitedBiometric policy tag and result in a BLOCK decision due to EU AI Act Article 5 prohibitions on untargeted facial database collection.'
    },
    {
      id: 'high-risk',
      title: 'Scenario B: High-Risk AI System',
      description: 'Test detection of high-risk AI systems requiring additional controls',
      input: {
        client_id: 'demo-client',
        user: 'demo-user',
        input_type: 'text',
        input: 'AI-powered CV screening system for automated recruitment decisions'
      },
      expected: {
        decision: 'flag',
        policy_tags: ['HighRiskAI'],
        risk_level: 'high'
      },
      explanation: 'This should trigger the HighRiskAI policy tag and result in a FLAG decision, requiring additional human oversight and controls under EU AI Act Annex III.'
    },
    {
      id: 'limited-risk',
      title: 'Scenario C: Limited Risk AI',
      description: 'Test detection of limited risk AI systems with transparency requirements',
      input: {
        client_id: 'demo-client',
        user: 'demo-user',
        input_type: 'text',
        input: 'Chatbot for customer service with emotion recognition capabilities'
      },
      expected: {
        decision: 'flag',
        policy_tags: ['LimitedRiskAI'],
        risk_level: 'limited'
      },
      explanation: 'This should trigger the LimitedRiskAI policy tag and result in a FLAG decision, requiring transparency and user notification under EU AI Act Article 52.'
    },
    {
      id: 'safe',
      title: 'Scenario D: Safe Content',
      description: 'Test that safe content is allowed through',
      input: {
        client_id: 'demo-client',
        user: 'demo-user',
        input_type: 'text',
        input: 'Weather forecast for tomorrow in London'
      },
      expected: {
        decision: 'allow',
        policy_tags: [],
        risk_level: 'minimal'
      },
      explanation: 'This should result in an ALLOW decision with minimal risk level, as it contains no prohibited or high-risk AI practices.'
    }
  ];

  const runScenario = (scenario) => {
    evaluateMutation.mutate({
      ...scenario.input,
      scenario: scenario.id
    });
  };

  const runAllScenarios = () => {
    demoScenarios.forEach((scenario, index) => {
      setTimeout(() => {
        runScenario(scenario);
        setCurrentStep(index + 1);
      }, index * 2000); // Run scenarios with 2-second delays
    });
  };

  const getDecisionIcon = (decision) => {
    switch (decision) {
      case 'block':
        return <XCircle className="h-5 w-5 text-red-600" />;
      case 'flag':
        return <AlertTriangle className="h-5 w-5 text-yellow-600" />;
      case 'allow':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
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

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Demo Scenarios</h1>
        <p className="text-gray-600">Scripted EU AI Act compliance demonstrations</p>
      </div>

      {/* Demo Controls */}
      <div className="actum-card-elevated">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Demo Controls</h2>
          <div className="flex space-x-2">
            <button
              onClick={runAllScenarios}
              disabled={evaluateMutation.isLoading}
              className="actum-button-primary flex items-center"
            >
              <Play className="h-4 w-4 mr-2" />
              Run All Scenarios
            </button>
          </div>
        </div>
        
        <div className="text-sm text-gray-600">
          <p>This demo showcases the EU AI Act compliance engine with scripted scenarios:</p>
          <ul className="list-disc list-inside mt-2 space-y-1">
            <li>Prohibited biometric practices detection</li>
            <li>High-risk AI system identification</li>
            <li>Limited risk AI transparency requirements</li>
            <li>Safe content validation</li>
          </ul>
        </div>
      </div>

      {/* Scenarios */}
      <div className="space-y-4">
        {demoScenarios.map((scenario, index) => {
          const result = results[scenario.id];
          const isRunning = evaluateMutation.isLoading && evaluateMutation.variables?.scenario === scenario.id;
          
          return (
            <div key={scenario.id} className={`actum-card-gradient ${result ? getDecisionColor(result.decision) : ''}`}>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="text-sm font-medium text-gray-500">Step {index + 1}</span>
                    <h3 className="text-lg font-semibold text-gray-900">{scenario.title}</h3>
                    {result && getDecisionIcon(result.decision)}
                  </div>
                  
                  <p className="text-sm text-gray-600 mb-3">{scenario.description}</p>
                  
                  <div className="actum-card-icon-bg rounded-md p-3 mb-3">
                    <p className="text-sm font-medium text-gray-700 mb-1">Input:</p>
                    <p className="text-sm text-gray-600 font-mono">{scenario.input.input}</p>
                  </div>

                  {result && (
                    <div className="space-y-2">
                      <div className="flex items-center space-x-4">
                        <span className={`actum-badge-modern ${
                          result.decision === 'block' ? 'text-red-600 bg-red-100' :
                          result.decision === 'flag' ? 'text-yellow-600 bg-yellow-100' :
                          result.decision === 'allow' ? 'text-green-600 bg-green-100' :
                          'text-gray-600 bg-gray-100'
                        }`}>
                          Decision: {result.decision.toUpperCase()}
                        </span>
                        <span className={`actum-badge-modern ${
                          result.risk_level === 'unacceptable' ? 'text-red-600 bg-red-100' :
                          result.risk_level === 'high' ? 'text-orange-600 bg-orange-100' :
                          result.risk_level === 'limited' ? 'text-yellow-600 bg-yellow-100' :
                          'text-green-600 bg-green-100'
                        }`}>
                          Risk: {result.risk_level}
                        </span>
                        <span className="text-sm text-gray-600">
                          Confidence: {result.confidence_score}%
                        </span>
                      </div>
                      
                      {result.policy_tags.length > 0 && (
                        <div>
                          <p className="text-sm font-medium text-gray-700 mb-1">Triggered Policies:</p>
                          <div className="flex flex-wrap gap-1">
                            {result.policy_tags.map((tag, tagIndex) => (
                              <span key={tagIndex} className="actum-badge-modern bg-red-100 text-red-800">
                                {tag}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                      
                      <div>
                        <p className="text-sm font-medium text-gray-700 mb-1">Explanation:</p>
                        <p className="text-sm text-gray-600">{result.explanation}</p>
                      </div>
                      
                      <div>
                        <p className="text-sm font-medium text-gray-700 mb-1">Expected vs Actual:</p>
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <p className="font-medium text-gray-700">Expected:</p>
                            <p className="text-gray-600">Decision: {scenario.expected.decision}</p>
                            <p className="text-gray-600">Risk: {scenario.expected.risk_level}</p>
                          </div>
                          <div>
                            <p className="font-medium text-gray-700">Actual:</p>
                            <p className="text-gray-600">Decision: {result.decision}</p>
                            <p className="text-gray-600">Risk: {result.risk_level}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  <div className="mt-4">
                    <p className="text-sm text-gray-600">{scenario.explanation}</p>
                  </div>
                </div>
                
                <div className="ml-4">
                  <button
                    onClick={() => runScenario(scenario)}
                    disabled={isRunning}
                    className="actum-button-secondary flex items-center"
                  >
                    {isRunning ? (
                      'Running...'
                    ) : (
                      <>
                        <ArrowRight className="h-4 w-4 mr-2" />
                        Run
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Demo Summary */}
      {Object.keys(results).length === demoScenarios.length && (
        <div className="actum-card-accent bg-blue-50">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Demo Summary</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 className="font-medium text-gray-900 mb-2">EU AI Act Compliance Features Demonstrated:</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Prohibited practices detection (Article 5)</li>
                <li>• High-risk AI system classification (Annex III)</li>
                <li>• Limited risk transparency requirements (Article 52)</li>
                <li>• Immutable audit trail with HMAC signatures</li>
                <li>• Policy-based decision making</li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Results Summary:</h3>
              <div className="text-sm text-gray-600 space-y-1">
                {demoScenarios.map(scenario => {
                  const result = results[scenario.id];
                  return (
                    <div key={scenario.id} className="flex justify-between">
                      <span>{scenario.title.split(':')[0]}:</span>
                      <span className={`font-medium ${
                        result.decision === scenario.expected.decision ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {result.decision.toUpperCase()}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Demo;
