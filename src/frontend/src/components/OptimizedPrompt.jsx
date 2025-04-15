import React, { useState, useRef } from 'react';

const CommentBox = ({ position, onSubmit, onCancel }) => {
  const [comment, setComment] = useState('');
  const inputRef = useRef(null);

  React.useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (comment.trim()) {
      onSubmit(comment);
      setComment('');
    }
  };

  const adjustPosition = () => {
    const viewportWidth = window.innerWidth;
    const boxWidth = 256;
    
    if (position.x + boxWidth > viewportWidth) {
      return {
        left: 'auto',
        right: `${viewportWidth - position.x + 10}px`,
        top: `${position.y}px`
      };
    }
    
    return {
      left: `${position.x}px`,
      top: `${position.y}px`
    };
  };

  return (
    <div 
      className="fixed bg-white rounded-lg shadow-lg border border-gray-200 p-2 w-64 z-50"
      style={adjustPosition()}
    >
      <form onSubmit={handleSubmit} className="space-y-2">
        <textarea
          ref={inputRef}
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          className="w-full p-2 text-sm border rounded-md focus:ring-2 focus:ring-indigo-500 
                   focus:border-indigo-500 resize-none"
          placeholder="Add your comment here..."
          rows="3"
        />
        <div className="flex justify-end space-x-2">
          <button
            type="button"
            onClick={onCancel}
            className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800 
                     rounded-md hover:bg-gray-100 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="px-3 py-1 text-sm text-white bg-indigo-600 
                     hover:bg-indigo-700 rounded-md transition-colors"
          >
            Add
          </button>
        </div>
      </form>
    </div>
  );
};

const CommentTooltip = ({ comment, position }) => {
  return (
    <div 
      className="fixed bg-white rounded-md shadow-lg border border-gray-200 p-3 w-64 z-50
                 text-sm text-gray-700 transform -translate-y-full"
      style={{
        left: `${position.x}px`,
        top: `${position.y}px`,
        marginTop: '-8px'
      }}
    >
      {comment}
    </div>
  );
};

const OptimizedPrompt = ({ optimizedText, comments, setComments, sessionId }) => {
  const [showCommentBox, setShowCommentBox] = useState(false);
  const [commentPosition, setCommentPosition] = useState({ x: 0, y: 0 });
  const [selectedRange, setSelectedRange] = useState(null);
  const [hoveredComment, setHoveredComment] = useState(null);
  const containerRef = useRef(null);

  const handleSelection = () => {
    const selection = window.getSelection();
    const selectedText = selection.toString().trim();

    if (!selectedText) {
      setShowCommentBox(false);
      return;
    }

    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();
    
    const x = rect.right;
    const y = rect.top;

    setCommentPosition({ x, y });
    setSelectedRange({
      text: selectedText,
      startOffset: range.startOffset,
      endOffset: range.endOffset
    });
    setShowCommentBox(true);
  };

  const handleCommentSubmit = async (commentText) => {
    try {
      console.log('Submitting feedback:', {  // Debug log
        text: selectedRange.text,
        startOffset: selectedRange.startOffset,
        endOffset: selectedRange.endOffset,
        feedback: commentText,
        promptId: sessionId
      });

      const response = await fetch('http://localhost:5000/comments', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: selectedRange.text,
          startOffset: selectedRange.startOffset,
          endOffset: selectedRange.endOffset,
          feedback: commentText,
          promptId: sessionId
        }),
      });

      const data = await response.json();
      console.log('Response from server:', data);  // Debug log

      if (!response.ok) {
        throw new Error(data.error || 'Failed to save feedback');
      }

      if (data.success) {
        const newComment = {
          id: data.comment.id,
          text: selectedRange.text,
          startOffset: selectedRange.startOffset,
          endOffset: selectedRange.endOffset,
          comment: commentText,
          created_at: new Date().toISOString()
        };
        setComments(prev => [...prev, newComment]);
      }
    } catch (error) {
      console.error('Error saving feedback:', error);
      alert('Failed to save feedback: ' + error.message);
    }
    
    setShowCommentBox(false);
    window.getSelection().removeAllRanges();
  };

  const renderTextWithHighlights = () => {
    if (!comments.length) return optimizedText;

    let lastIndex = 0;
    const pieces = [];
    const sortedComments = [...comments].sort((a, b) => a.startOffset - b.startOffset);

    sortedComments.forEach((comment, index) => {
      if (comment.startOffset > lastIndex) {
        pieces.push(
          <span key={`text-${index}`} className="font-mono">
            {optimizedText.slice(lastIndex, comment.startOffset)}
          </span>
        );
      }

      pieces.push(
        <span
          key={comment.id}
          className="bg-yellow-100 hover:bg-yellow-200 cursor-pointer transition-colors 
                   relative font-mono"
          onMouseEnter={(e) => {
            const rect = e.target.getBoundingClientRect();
            setHoveredComment({
              comment: comment.comment,
              position: {
                x: rect.left,
                y: rect.top + window.scrollY
              }
            });
          }}
          onMouseLeave={() => {
            setHoveredComment(null);
          }}
        >
          {optimizedText.slice(comment.startOffset, comment.endOffset)}
        </span>
      );

      lastIndex = comment.endOffset;
    });

    if (lastIndex < optimizedText.length) {
      pieces.push(
        <span key="text-end" className="font-mono">
          {optimizedText.slice(lastIndex)}
        </span>
      );
    }

    return pieces;
  };

  return (
    <div className="relative" ref={containerRef}>
      <div 
        onMouseUp={handleSelection}
        className="text-gray-700 text-lg whitespace-pre-wrap font-mono leading-relaxed"
        style={{
          fontFamily: "'Consolas', 'Monaco', 'Courier New', monospace",
        }}
      >
        {renderTextWithHighlights()}
      </div>
      
      {showCommentBox && (
        <CommentBox
          position={commentPosition}
          onSubmit={handleCommentSubmit}
          onCancel={() => setShowCommentBox(false)}
        />
      )}

      {hoveredComment && (
        <CommentTooltip
          comment={hoveredComment.comment}
          position={hoveredComment.position}
        />
      )}
    </div>
  );
};

export default OptimizedPrompt; 