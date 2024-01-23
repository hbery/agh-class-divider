import React, { useRef, useState } from 'react';
import axios from 'axios';
import {
    AppContainer,
    MainPageWrapper,
    Logo,
    SelectFileWrapper,
    SelectFileButton,
    ConfirmButtonWrapper,
    ConfirmButton,
    Icon,
    SelectScheduleWrapper,
    SelectGroupWrapper,
    GroupIcon,
    ScheduleIcon,
    SelectFileTitle,
    LogoWrapper,
    SelectedFileNameWrapper,
    SelectedFileName,
    FileInputContainer,
    AttachmentIcon,
    SuccessMessageWrapper,
    DownloadButton,
    DownloadIcon,
    DownloadWrapper,
    SuccessImage,
    DownloadTitle,
    RetryButton,
    RetryIcon,
    DownloadButtonsWrapper,
    LoadingWrapper,
    LoadingIcon,
    LoadingTitle
} from './MainPageElements';
import schedule from '../../images/schedule.png';
import group from '../../images/group.png';
import logo from '../../images/logo.png';
import success from '../../images/success.png';


const MainPage = () => {
    const scheduleFileInputRef = useRef(null);
    const groupFileInputRef = useRef(null);
    const [selectedScheduleFile, setSelectedScheduleFile] = useState(null);
    const [selectedGroupFile, setSelectedGroupFile] = useState(null);
    const [confirmationState, setConfirmationState] = useState(false);
    const [jobId, setJobId] = useState(null);
    const BASE_URL = "http://127.0.0.1:8000";

    const [loading, setLoading] = useState(false);


    const handleSelectScheduleFile = () => {
        scheduleFileInputRef.current.click();
    };

    const handleScheduleFileChange = (event) => {
        const file = event.target.files[0];
        setSelectedScheduleFile(file);
        // Handle the selected file
        console.log('Selected Schedule File:', file);
    };

    const handleSelectGroupFile = () => {
        groupFileInputRef.current.click();
    };

    const handleGroupFileChange = (event) => {
        const file = event.target.files[0];
        setSelectedGroupFile(file);
        // Handle the selected file
        console.log('Selected Group File:', file);
    };

    const handleConfirmButtonClick = async () => {
        if (selectedScheduleFile && selectedGroupFile) {
            try {
                setLoading(true);

                // Step 1: Create a job
                const createJobResponse = await axios.post(`${BASE_URL}/jobs/create`);
                const jobId = createJobResponse.data.job_id;
                setJobId(jobId); // Store the job_id in the state

                // Step 2: Upload schedule file
                const scheduleFormData = new FormData();
                scheduleFormData.append('file', selectedScheduleFile);
                await axios.post(`${BASE_URL}/schedule/file?jobid=${jobId}`, scheduleFormData);

                // Step 3: Upload group file
                const groupFormData = new FormData();
                groupFormData.append('file', selectedGroupFile);
                await axios.post(`${BASE_URL}/preferences/file?jobid=${jobId}`, groupFormData);

                // Step 4: Prepare model
                await axios.post(`${BASE_URL}/jobs/${jobId}/prepare`);

                // Step 5: Run the model
                await axios.post(`${BASE_URL}/jobs/${jobId}/run`);

                // Update confirmation state
                setConfirmationState(true);

                setLoading(false);
            } catch (error) {
                console.error('Error:', error);

                setLoading(false);

                if (axios.isAxiosError(error)) {
                    // Axios specific error handling
                    console.error('Axios error details:', error.response);
                }

                window.alert('An error occurred during the API calls.');
            }
        } else {
            window.alert('Please select both files before continuing.');
        }
    };

    const isConfirmButtonActive = selectedScheduleFile && selectedGroupFile;

    const handleDownloadClick = async () => {
        try {
            if (jobId) {
                // Step 1: Make a GET request to download the file using the stored job_id
                const downloadResponse = await axios.get(`${BASE_URL}/results/${jobId}/schedule/file`, { responseType: 'blob' });

                // Step 2: Create a Blob from the downloaded data
                const blob = new Blob([downloadResponse.data], { type: 'application/octet-stream' });

                // Step 3: Create a URL for the Blob
                const url = window.URL.createObjectURL(blob);

                // Step 4: Create an anchor element and trigger the download
                const a = document.createElement('a');
                a.href = url;
                a.download = `test-${jobId}.csv`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);

                // Optionally, you can revoke the Blob URL to free up resources
                window.URL.revokeObjectURL(url);
            } else {
                window.alert('Job ID not available. Please confirm the job first.');
            }
        } catch (error) {
            console.error('Error:', error);
            window.alert('An error occurred while downloading the file.');
        }
    };

    const handleRetryClick = () => {
        setConfirmationState(false);
    };

    return (
        <AppContainer>
            <MainPageWrapper>
                <LogoWrapper>
                    <Logo src={logo} alt="Class Divider" />
                </LogoWrapper>
                {loading ? (
                    <LoadingWrapper>
                        <LoadingIcon />
                        <LoadingTitle>Tworzenie pliku...</LoadingTitle>
                    </LoadingWrapper>
                ) : confirmationState ? (
                    <DownloadWrapper>
                    <SuccessMessageWrapper>
                        <SuccessImage src={success} alt="Success!" />
                        <DownloadTitle>
                            <strong>Udało się!</strong>{'\n'}Plik z gotowym podziałem jest gotowy do pobrania.
                        </DownloadTitle>
                        <DownloadButtonsWrapper>
                            <DownloadButton onClick={handleDownloadClick}>
                                <DownloadIcon />
                                Pobierz plik
                            </DownloadButton>
                            <RetryButton onClick={handleRetryClick}>
                                <RetryIcon />
                            </RetryButton>
                        </DownloadButtonsWrapper>
                    </SuccessMessageWrapper>
                    </DownloadWrapper>
            ) : (
            <MainPageWrapper>
                <SelectFileWrapper>
                    <SelectScheduleWrapper>
                        <ScheduleIcon src={schedule} alt="Schedule file" />
                        <SelectFileTitle>Wybierz plik z planem zajęć</SelectFileTitle>
                        <FileInputContainer>
                            <AttachmentIcon alt="Attachment icon" />
                            <input
                                type="file"
                                accept=".csv"
                                style={{ display: 'none' }}
                                ref={scheduleFileInputRef}
                                onChange={handleScheduleFileChange}
                            />
                            {selectedScheduleFile && (
                                <SelectedFileName>
                                    {selectedScheduleFile.name.slice(0, 20)}{selectedScheduleFile.name.length > 20 ? '...' : ''}
                                </SelectedFileName>
                            )}
                        </FileInputContainer>
                    </SelectScheduleWrapper>
                    <SelectGroupWrapper>
                        <GroupIcon src={group} alt="Group file" />
                        <SelectFileTitle>Wybierz plik z danymi studentów</SelectFileTitle>
                        <FileInputContainer>
                            <AttachmentIcon alt="Attachment icon" />
                            <input
                                type="file"
                                accept=".csv"
                                style={{ display: 'none' }}
                                ref={groupFileInputRef}
                                onChange={handleGroupFileChange}
                            />
                            {selectedGroupFile && (
                                <SelectedFileName>{selectedGroupFile.name.slice(0, 20)}{selectedGroupFile.name.length > 20 ? '...' : ''}</SelectedFileName>
                            )}
                        </FileInputContainer>
                    </SelectGroupWrapper>
                </SelectFileWrapper>
                <ConfirmButtonWrapper>
                    <ConfirmButton
                        onClick={handleConfirmButtonClick}
                        disabled={!isConfirmButtonActive}
                        style={{
                            cursor: isConfirmButtonActive ? 'pointer' : 'not-allowed',
                            opacity: isConfirmButtonActive ? 1 : 0.5,
                        }}
                    >
                        Kontynuuj
                    </ConfirmButton>
                </ConfirmButtonWrapper>
            </MainPageWrapper>
                )}

        </MainPageWrapper>
        </AppContainer >
    );
};

export default MainPage;
