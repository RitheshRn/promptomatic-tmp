import React, { useState, useRef } from 'react';
import CommentPopover from '../src/components/CommentPopover';

const OptimizedPrompt = ({ optimizedText }) => {
  const [comments, setComments] = useState([]);
  const [selectedText, setSelectedText] = useState(null);
  const [showCommentPopover, setShowCommentPopover] = useState(false);
  const [popoverPosition, setPopoverPosition] = useState({ x: 0, y: 0 });
  const containerRef = useRef(null);

  const handleTextSelection = () => {
    const selection = window.getSelection();
    if (selection.toString().length > 0) {
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      const containerRect = containerRef.current.getBoundingClientRect();

      setSelectedText({
        text: selection.toString(),
        startOffset: range.startOffset,
        endOffset: range.endOffset
      });

      setPopoverPosition({
        x: rect.left - containerRect.left,
        y: rect.bottom - containerRect.top + 10
      });

      setShowCommentPopover(true);
    }
  };

  const handleSaveComment = (commentText) => {
    if (selectedText) {
      setComments([
        ...comments,
        {
          ...selectedText,
          comment: commentText,
          id: Date.now()
        }
      ]);
    }
    setSelectedText(null);
  };

  const renderTextWithComments = () => {
    let result = optimizedText;
    const sortedComments = [...comments].sort((a, b) => b.startOffset - a.startOffset);

    sortedComments.forEach(comment => {
      const before = result.slice(0, comment.startOffset);
      const highlighted = result.slice(comment.startOffset, comment.endOffset);
      const after = result.slice(comment.endOffset);

      result = (
        <>
          {before}
          <span 
            className="bg-yellow-100 cursor-pointer relative group"
            title={comment.comment}
          >
            {highlighted}
            <span className="absolute bottom-full left-0 bg-gray-800 text-white p-2 rounded-md hidden group-hover:block whitespace-nowrap">
              {comment.comment}
            </span>
          </span>
          {after}
        </>
      );
    });

    return result;
  };

  return (
    <div 
      ref={containerRef}
      className="relative p-4 bg-white rounded-lg shadow"
    >
      <div 
        onMouseUp={handleTextSelection}
        className="prose max-w-none"
      >
        {renderTextWithComments()}
      </div>

      {showCommentPopover && (
        <CommentPopover
          position={popoverPosition}
          onClose={() => setShowCommentPopover(false)}
          onSave={handleSaveComment}
        />
      )}
    </div>
  );
};

export default OptimizedPrompt; 