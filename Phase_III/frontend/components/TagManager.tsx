import React, { useState, useEffect } from "react";
import { Tag } from "@/types";
import { api } from "@/lib/api";
import { websocketService } from "@/lib/websocket";

interface TagManagerProps {
    userId: string;
    selectedTagIds?: number[];
    onSelectTags?: (tagIds: number[]) => void;
    showSelector?: boolean;
    showManager?: boolean;
}

const TagManager: React.FC<TagManagerProps> = ({
    userId,
    selectedTagIds = [],
    onSelectTags,
    showSelector = true,
    showManager = true,
}) => {
    const [tags, setTags] = useState<Tag[]>([]);
    const [newTagName, setNewTagName] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        loadTags();

        // Subscribe to tag updates
        const unsubscribe = websocketService.subscribeToTagUpdates(
            (tag, type) => {
                if (
                    type === "tag_create" ||
                    type === "collaboration_tag_create"
                ) {
                    setTags((prev) => [...prev, tag]);
                } else if (
                    type === "tag_update" ||
                    type === "collaboration_tag_update"
                ) {
                    setTags((prev) =>
                        prev.map((t) => (t.id === tag.id ? tag : t)),
                    );
                } else if (
                    type === "tag_delete" ||
                    type === "collaboration_tag_delete"
                ) {
                    setTags((prev) => prev.filter((t) => t.id !== tag.id));
                    // Remove the deleted tag from selected tags if it was selected
                    if (selectedTagIds.includes(tag.id) && onSelectTags) {
                        onSelectTags(
                            selectedTagIds.filter((id) => id !== tag.id),
                        );
                    }
                }
            },
        );

        return () => {
            unsubscribe();
        };
    }, [userId]); // Only userId is needed as dependency, not selectedTagIds or onSelectTags

    const loadTags = async () => {
        try {
            setLoading(true);
            const tagsData = await api.getTags(userId);
            setTags(tagsData);
            setError(null);
        } catch (err) {
            console.error("Error loading tags:", err);
            setError("Failed to load tags");
        } finally {
            setLoading(false);
        }
    };

    const handleCreateTag = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newTagName.trim()) return;

        try {
            const newTag = await api.createTag(userId, {
                name: newTagName.trim(),
            });

            // Send collaboration event
            websocketService.sendCollaborationEvent("tag_create", newTag);

            setNewTagName("");
        } catch (err) {
            console.error("Error creating tag:", err);
            setError("Failed to create tag");
        }
    };

    const handleDeleteTag = async (tagId: number) => {
        if (
            !window.confirm(
                "Are you sure you want to delete this tag? This will remove it from all tasks.",
            )
        ) {
            return;
        }

        try {
            await api.deleteTag(userId, tagId);
            // Directly update the state since WebSocket is not supported in Phase II
            setTags(prev => prev.filter(tag => tag.id !== tagId));
            // Remove the deleted tag from selected tags if it was selected
            if (selectedTagIds.includes(tagId) && onSelectTags) {
                onSelectTags(
                    selectedTagIds.filter((id) => id !== tagId),
                );
            }
            // Send collaboration event for compatibility (though it won't do anything in Phase II)
            websocketService.sendCollaborationEvent("tag_delete", {
                id: tagId,
            });
        } catch (err) {
            console.error("Error deleting tag:", err);
            setError("Failed to delete tag");
        }
    };

    const handleTagToggle = (tagId: number) => {
        let newSelectedTagIds;
        if (selectedTagIds.includes(tagId)) {
            newSelectedTagIds = selectedTagIds.filter((id) => id !== tagId);
        } else {
            newSelectedTagIds = [...selectedTagIds, tagId];
        }

        if (onSelectTags) {
            onSelectTags(newSelectedTagIds);
        }
    };

    if (loading && showSelector) {
        return <div>Loading tags...</div>;
    }

    return (
        <div className="space-y-4">
            {showSelector && (
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Tags
                    </label>
                    <div className="flex flex-wrap gap-2">
                        {tags.map((tag) => (
                            <div
                                key={tag.id}
                                className="flex items-center group"
                            >
                                <button
                                    type="button"
                                    className={`px-3 py-1 rounded-full text-sm ${
                                        selectedTagIds.includes(tag.id)
                                            ? "bg-blue-100 text-blue-800 border border-blue-300"
                                            : "bg-gray-100 text-gray-800 border border-gray-300 hover:bg-gray-200"
                                    }`}
                                    onClick={() => handleTagToggle(tag.id)}
                                >
                                    #{tag.name}
                                </button>
                                <button
                                    type="button"
                                    className="ml-1 text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
                                    onClick={() => handleDeleteTag(tag.id)}
                                    title="Delete tag"
                                >
                                    ×
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {showManager && (
                <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                    <h3 className="text-lg font-medium text-gray-900 mb-3">
                        Manage Tags
                    </h3>

                    {error && (
                        <div className="mb-3 p-2 bg-red-100 text-red-700 rounded">
                            {error}
                        </div>
                    )}

                    <form
                        onSubmit={handleCreateTag}
                        className="flex flex-col sm:flex-row gap-2 mb-3"
                    >
                        <input
                            type="text"
                            value={newTagName}
                            onChange={(e) => setNewTagName(e.target.value)}
                            placeholder="New tag name (without #)"
                            className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                            maxLength={50}
                        />
                        <button
                            type="submit"
                            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                            Add Tag
                        </button>
                    </form>

                    <div className="space-y-2">
                        {tags.map((tag) => (
                            <div
                                key={tag.id}
                                className="flex items-center justify-between p-2 bg-white rounded border"
                            >
                                <span>#{tag.name}</span>
                                <button
                                    type="button"
                                    className="text-red-500 hover:text-red-700"
                                    onClick={() => handleDeleteTag(tag.id)}
                                >
                                    Delete
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default TagManager;
