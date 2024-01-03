import React from 'react';
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
} from './MainPageElements';
import schedule from '../../images/schedule.png';
import group from '../../images/group.png';
import logo from '../../images/logo.png';


const MainPage = () => {
    const handleSelectScheduleFile = () => {
        // Implement file selection logic for schedule file
        console.log('Select Schedule File');
    };

    const handleSelectGroupFile = () => {
        // Implement file selection logic for group file
        console.log('Select Group File');
    };

    const handleConfirmButtonClick = () => {
        // Implement logic for confirm button click
        console.log('Confirm Button Clicked');
    };

    return (
        <AppContainer>
            <MainPageWrapper>
                <LogoWrapper>
                    <Logo src={logo} alt="Class Divider"/>
                </LogoWrapper>
                <SelectFileWrapper>
                    <SelectScheduleWrapper>
                        <ScheduleIcon src={schedule} alt="Schedule file" />
                        <SelectFileTitle>Select a schedule file</SelectFileTitle>
                        <SelectFileButton onClick={handleSelectScheduleFile}>
                            Select
                        </SelectFileButton>
                    </SelectScheduleWrapper>
                    <SelectGroupWrapper>
                    <GroupIcon src={group} alt="Group file" />
                        <SelectFileTitle>Choose the user data file</SelectFileTitle>
                        <SelectFileButton onClick={handleSelectGroupFile}>
                            Select
                        </SelectFileButton>
                    </SelectGroupWrapper>
                </SelectFileWrapper>
                <ConfirmButtonWrapper>
                    <ConfirmButton onClick={handleConfirmButtonClick}>
                        Process
                    </ConfirmButton>
                </ConfirmButtonWrapper>
            </MainPageWrapper>
        </AppContainer>
    );
};

export default MainPage;
