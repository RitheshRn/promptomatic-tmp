import React, { useState } from 'react';
import { Card, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';
import OptimizedPrompt from './OptimizedPrompt';

const PromptOptimizer = () => {
  const [input, setInput] = useState('');
  const [optimizedPrompt, setOptimizedPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [error, setError] = useState(null);
  const [comments, setComments] = useState([]);
  const [response, setResponse] = useState(null);

  const clearComments = () => {
    setComments([]);
    if (window.getSelection) {
      window.getSelection().removeAllRanges();
    }
  };

  const startNewSession = () => {
    setInput('');
    setOptimizedPrompt('');
    setSessionId(null);
    setError(null);
    setResponse(null);
    clearComments();
  };

  const handleOptimize = async () => {
    try {
      setIsLoading(true);
      console.log("Sending request with input:", input);  // Debug log

      const response = await fetch('http://localhost:5000/optimize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          human_input: input,
        }),
      });

      const data = await response.json();
      console.log("Raw response data:", data);  // Debug log

      if (!data) {
        console.error("No data received");  // Debug log
        throw new Error('No data received from server');
      }

      if (data.error) {
        console.error("Error in response:", data.error);  // Debug log
        throw new Error(data.error);
      }

      // Create a new state object
      const newState = {};

      // Only update if we have valid data
      if (typeof data.result === 'string') {
        console.log("Setting optimized prompt:", data.result);  // Debug log
        newState.optimizedPrompt = data.result;
        setOptimizedPrompt(data.result);
      } else {
        console.warn("Invalid or missing result in response");  // Debug log
      }

      if (data.session_id) {
        console.log("Setting session ID:", data.session_id);  // Debug log
        newState.sessionId = data.session_id;
        setSessionId(data.session_id);
      }

      if (data.metrics) {
        console.log("Setting metrics:", data.metrics);  // Debug log
        newState.response = data;
        setResponse(data);
      }

      setError(null);
      clearComments();

      // Log final state
      console.log("Final state after updates:", {
        ...newState,
        currentOptimizedPrompt: optimizedPrompt,
        currentSessionId: sessionId,
        currentResponse: response
      });

    } catch (err) {
      console.error("Optimization error:", err);  // Debug log
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleOptimizeWithFeedback = async () => {
    if (!sessionId) {
      setError('No active optimization session. Please optimize first.');
      return;
    }

    try {
      setIsLoading(true);
      const response = await fetch('http://localhost:5000/optimize-with-feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
        }),
      });

      const data = await response.json();
      console.log("Feedback optimization response:", data);  // Debug log

      if (data.error) {
        throw new Error(data.error);
      }

      // Only update if we have valid data
      if (typeof data.result === 'string') {
        console.log("Setting optimized prompt:", data.result);  // Debug log
        setOptimizedPrompt(data.result);
      } else {
        console.warn("Invalid or missing result in feedback response");  // Debug log
      }

      if (data.metrics) {
        console.log("Setting metrics:", data.metrics);  // Debug log
        setResponse(data);
      }

      clearComments();
      setError(null);

    } catch (err) {
      console.error("Feedback optimization error:", err);  // Debug log
      setError(err.message);
      // Keep existing state on error
      setOptimizedPrompt(prev => prev);
      setResponse(prev => prev);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadLog = async () => {
    if (!sessionId) {
      setError('No active session to download logs from.');
      return;
    }

    try {
      console.log('Attempting to download log for session:', sessionId);
      const response = await fetch(`http://localhost:5000/session/${sessionId}/log`);
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to download session log');
      }
      
      const contentType = response.headers.get('content-type');
      console.log('Response content type:', contentType);
      
      const blob = await response.blob();
      console.log('Blob size:', blob.size);
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `session_${sessionId}_log.txt`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error('Error downloading log:', err);
      setError(err.message);
    }
  };

  // Debug log for render
  console.log("Current state:", {
    optimizedPrompt,
    sessionId,
    response,
    error,
    isLoading
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-50 via-indigo-50 to-purple-50 p-8">
      <div className="max-w-7xl mx-auto space-y-12">
        {/* Centered Title with Wand */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-mono font-bold text-gray-800 flex items-center justify-center gap-3">
            <img 
              src="/images/logo1.png"
              alt="Promptomatic Logo" 
              className="h-12 w-auto"  // Increased from h-8 to h-12
            />
            Promptomatic
          </h1>
        </div>

        {/* Error Display - Brighter red */}
        {error && (
          <div className="bg-red-100 border-l-4 border-red-400 text-red-700 p-4 rounded-lg shadow-sm">
            <div className="flex">
              <div className="ml-3">
                <p className="font-mono text-sm">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Main Content - Side by Side Layout */}
        <div className="grid grid-cols-2 gap-8">
          {/* Input Section */}
          <Card className="shadow-lg hover:shadow-xl transition-shadow duration-300 bg-white/80 border border-indigo-100">
            <CardContent className="p-8">
              <div className="space-y-8">
                <h2 className="text-2xl font-mono font-bold text-indigo-800 text-center mt-4">
                  Enter Your Prompt
                </h2>
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  className="w-full h-[calc(100vh-600px)] min-h-[300px] p-6 border border-indigo-200 
                           rounded-xl focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 
                           text-gray-700 font-mono text-lg shadow-inner bg-white/90 
                           hover:bg-white transition-colors duration-200"
                  placeholder="Enter your prompt here..."
                  style={{ resize: 'vertical', fontFamily: 'monospace' }}
                />
                
                {/* Initial Prompt Score Section */}
                {response?.metrics && (
                  <div className="p-4 border border-gray-200 rounded-lg">
                    <h3 className="text-lg font-semibold mb-3">
                      Initial Prompt Score
                    </h3>
                    <div>
                      <p className="text-sm font-medium mb-2">
                        Score: {response.metrics.initial_prompt_score}%
                      </p>
                      <div className="w-full bg-gray-200 rounded-full h-2.5">
                        <div 
                          className="bg-blue-600 h-2.5 rounded-full transition-all duration-500"
                          style={{ width: `${response.metrics.initial_prompt_score}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Output Section */}
          {optimizedPrompt || isLoading ? (
            <Card className="shadow-lg hover:shadow-xl transition-shadow duration-300 bg-white/80 border border-indigo-100">
              <CardContent className="p-8">
                <div className="space-y-8">
                  <h2 className="text-2xl font-mono font-bold text-indigo-800 text-center mt-4">
                    {optimizedPrompt ? 'Optimized Prompt' : 'Waiting for optimization...'}
                  </h2>
                  <div className="bg-white/90 rounded-xl p-6 h-[calc(100vh-600px)] min-h-[300px] overflow-auto border border-indigo-200">
                    {optimizedPrompt ? (
                      <OptimizedPrompt 
                        optimizedText={optimizedPrompt}
                        comments={comments}
                        setComments={setComments}
                        sessionId={sessionId}
                      />
                    ) : (
                      <p className="text-indigo-400 text-lg italic font-mono">
                        Optimizing your prompt...
                      </p>
                    )}
                  </div>
                  
                  {/* Optimized Prompt Score Section */}
                  {response?.metrics && (
                    <div className="p-4 border border-gray-200 rounded-lg">
                      <h3 className="text-lg font-semibold mb-3">
                        Optimized Prompt Score
                      </h3>
                      <div>
                        <p className="text-sm font-medium mb-2">
                          Score: {response.metrics.optimized_prompt_score}%
                        </p>
                        <div className="w-full bg-gray-200 rounded-full h-2.5">
                          <div 
                            className="bg-green-600 h-2.5 rounded-full transition-all duration-500"
                            style={{ width: `${response.metrics.optimized_prompt_score}%` }}
                          ></div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          ) : (
            <div className="flex items-center justify-center h-full">
              <p className="text-indigo-400 text-lg italic font-mono">
                Click "Optimize Prompt" to start optimization
              </p>
            </div>
          )}
        </div>

        {/* Optimization Buttons */}
        <div className="grid grid-cols-2 gap-8 mt-4">
          {/* Initial Optimization Button - Always visible */}
          <Button 
            onClick={handleOptimize}
            className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 
                     hover:to-cyan-600 text-white py-3 rounded-xl text-lg font-mono
                     transform transition-all duration-200 hover:scale-105 shadow-md 
                     hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={isLoading}
            style={{ fontFamily: 'monospace' }}
          >
            {isLoading ? (
              <span className="flex items-center justify-center font-mono">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Optimizing...
              </span>
            ) : 'Optimize Prompt'}
          </Button>

          {/* Feedback Optimization Button - Only visible after first optimization */}
          {sessionId && (
            <Button 
              onClick={handleOptimizeWithFeedback}
              className="w-full bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 
                       hover:to-emerald-600 text-white py-3 rounded-xl text-lg font-mono
                       transform transition-all duration-200 hover:scale-105 shadow-md 
                       hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={isLoading}
              style={{ fontFamily: 'monospace' }}
            >
              {isLoading ? (
                <span className="flex items-center justify-center font-mono">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Optimizing...
                </span>
              ) : 'Optimize with Feedback'}
            </Button>
          )}
        </div>

        {/* Session Buttons */}
        <div className="flex justify-center gap-4">
          <Button 
            onClick={startNewSession}
            className="bg-gradient-to-r from-indigo-400 to-indigo-500 hover:from-indigo-500 
                     hover:to-indigo-600 text-white px-8 py-2 rounded-xl transition-all 
                     duration-200 ease-in-out transform hover:scale-105 shadow-md 
                     hover:shadow-lg font-mono"
            disabled={isLoading}
          >
            New Session
          </Button>
          
          {sessionId && (
            <Button 
              onClick={handleDownloadLog}
              className="bg-gradient-to-r from-violet-400 to-violet-500 hover:from-violet-500 
                       hover:to-violet-600 text-white px-8 py-2 rounded-xl transition-all 
                       duration-200 ease-in-out transform hover:scale-105 shadow-md 
                       hover:shadow-lg font-mono"
              disabled={isLoading}
            >
              Download Session Log
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};

export default PromptOptimizer;