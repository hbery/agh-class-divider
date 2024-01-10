import React, { useRef, useState } from 'react';
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
    DownloadButtonsWrapper
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

    const handleConfirmButtonClick = () => {
        if (selectedScheduleFile && selectedGroupFile) {
            setConfirmationState(true);
            console.log('Confirm Button Clicked');
        } else {
            window.alert('Please select both files before continuing.');
        }
    };

    const isConfirmButtonActive = selectedScheduleFile && selectedGroupFile;

    const handleDownloadClick = () => {
        // Implement logic to trigger download
        console.log('Download Button Clicked');
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
                {confirmationState ? (
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
                                    accept=".xlsx"
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
                                    accept=".xlsx"
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
        </AppContainer>
    );
};

export default MainPage;
