import streamlit as st
import os
import cv2
from pathlib import Path


def save_video(uploaded_file):
    # Create videos directory if it doesn't exist
    if not os.path.exists("videos"):
        os.makedirs("videos")

    # Save the uploaded file
    file_path = os.path.join("videos", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def get_video_info(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    cap.release()
    return fps, duration


def main():
    st.title("Video Upload and Search App")

    # Upload section
    st.header("Upload Video")
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])

    if uploaded_file is not None:
        file_path = save_video(uploaded_file)
        st.success(f"Video uploaded successfully: {uploaded_file.name}")

        # Display video info
        fps, duration = get_video_info(file_path)
        st.write(f"FPS: {fps:.2f}")
        st.write(f"Duration: {duration:.2f} seconds")

        # Display video
        st.video(file_path)

    # Search section
    st.header("Search Videos")
    search_term = st.text_input("Enter video name to search")

    if search_term:
        videos = Path("videos").glob("*")
        found_videos = [video for video in videos if search_term.lower() in video.name.lower()]

        if found_videos:
            st.write(f"Found {len(found_videos)} videos:")
            for video in found_videos:
                st.write(video.name)
                st.video(str(video))
        else:
            st.warning("No videos found matching your search.")


if __name__ == "__main__":
    main()
