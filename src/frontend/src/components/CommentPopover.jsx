import React from 'react';
import { Button } from './ui/button';
import { X } from 'lucide-react';

const CommentPopover = ({ position, onClose, onSave }) => {
  const [comment, setComment] = React.useState('');

  const handleSave = () => {
    onSave(comment);
    onClose();
  };

  return (
    <div 
      className="fixed z-50 bg-white rounded-lg shadow-lg border p-4 w-80"
      style={{
        left: `${position.x}px`,
        top: `${position.y}px`
      }}
    >
      <div className="flex flex-col gap-2">
        <div className="flex justify-between items-center">
          <h3 className="font-medium">Add Comment</h3>
          <button 
            className="p-1 hover:bg-gray-100 rounded-full"
            onClick={onClose}
          >
            <X className="h-4 w-4" />
          </button>
        </div>
        <textarea
          className="min-h-[100px] w-full p-2 border rounded-md"
          placeholder="Enter your comment..."
          value={comment}
          onChange={(e) => setComment(e.target.value)}
        />
        <Button 
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2"
          onClick={handleSave}
        >
          Save Comment
        </Button>
      </div>
    </div>
  );
};

export default CommentPopover; 