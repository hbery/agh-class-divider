import styled from 'styled-components';
import { GrAttachment } from "react-icons/gr";
import { PiDownloadSimpleLight } from "react-icons/pi";
import { VscRefresh } from "react-icons/vsc";

export const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #F2F1EB;
`;

export const MainPageWrapper = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`;

export const LogoWrapper = styled.div`
display: flex;
justify-content: center;
align-items: center;
/* border: solid pink 1px; */
margin-right: -45px;
/* width: 80%; */
`;

export const Logo = styled.img`
`;


export const SelectFileWrapper = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 60em;
  margin-bottom: 20px;
  gap: 3em;
  padding: 1em;
  
`;

export const SelectFileTitle = styled.p`
  width: 70%;
  text-align: center;
  font-weight: 600;
  /* font-size: clamp(1.1em, 1vh, 1.3em); */
  font-size: 1.1em;
  color: #26190a;
`;

export const SelectScheduleWrapper = styled.div`
display: flex;
flex-direction: column;
justify-content: center;
align-items: center;
background-color: #ABC4AA;
padding: 1em;
border-radius: 1.2em;
/* border: 1px #698269 solid; */
min-width: 16em;
height: 18em;
box-shadow: 0 10px 12px rgba(0, 0, 0, 0.3);
`;

export const SelectGroupWrapper = styled.div`
display: flex;
justify-content: center;
align-items: center;
flex-direction: column;
background-color: #ABC4AA;
padding: 1em;
border-radius: 1.2em;
/* border: 1px #698269 solid; */
min-width: 16em;
height: 18em;
box-shadow: 0 10px 12px rgba(0, 0, 0, 0.3);
`;


export const ScheduleIcon = styled.img`
max-width: 30%;
max-height: 30%;
`;

export const GroupIcon = styled.img`
max-width: 33%;
max-height: 30%;
`;

export const SelectFileButton = styled.button`
  background-color: #A9907E;
  color: white;
  padding: 0.9em;
  border: none;
  border-radius: 1em;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);

  &:hover {
        background-color: #BFB29E;
    }
`;

export const ConfirmButtonWrapper = styled.div`
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;

`;

export const ConfirmButton = styled.button`
  min-width: 180%;
  min-height: 120%;
  background-color: #037060;
  color: white;
  font-size: 1em;
  /* color: black; */
  padding: 0.6em;
  border: none;
  border-radius: 1em;
  cursor: pointer;
  box-shadow: 0 10px 12px rgba(0, 0, 0, 0.3);

  &:hover, &:focus {
        background-color: #129683;
    }
`;

export const SelectedFileNameWrapper = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
`;


export const SelectedFileName = styled.p`
  width: 100%;
  text-align: center;  
  white-space: pre-line;
  overflow: hidden;
  text-overflow: ellipsis;
`;

export const FileInputContainer = styled.label`
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5em;
  cursor: pointer;
  background-color: #A9907E;
  color: white;
  padding: 0.9em;
  border-radius: 1em;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);

  &:hover {
    background-color: #BFB29E;
  }
`;

export const AttachmentIcon = styled(GrAttachment)`
  width: 20px;
  height: 20px;
`;

export const SuccessMessageWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1em;
`;

export const DownloadWrapper = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  background-color: #ABC4AA;
  padding: 1em;
  border-radius: 1.2em;
  width: 50%;
  /* min-width: 16em;
  height: 18em; */
  box-shadow: 0 10px 12px rgba(0, 0, 0, 0.3);
  padding: 4em 0.2em;
`;

export const DownloadButton = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;
  min-width: 110%;
  min-height: 120%;
  background-color: #037060;
  color: white;
  font-size: 1em;
  padding: 0.6em;
  border: none;
  border-radius: 1em;
  cursor: pointer;
  box-shadow: 0 10px 12px rgba(0, 0, 0, 0.3);

  &:hover, &:focus {
        background-color: #129683;
    }
  
`;

export const DownloadTitle = styled.p`
  width: 70%;
  text-align: center;
  /* font-weight: 600; */
  /* font-size: clamp(1.1em, 1vh, 1.3em); */
  font-size: 1.1em;
  color: #26190a;
  white-space: pre-line; 
`;

export const SuccessImage = styled.img`
  max-width: 33%;
  max-height: 30%;
`;

export const DownloadIcon = styled(PiDownloadSimpleLight)`
  margin-right: 0.5em;
  width: 25px;
  height: 25px;   
`;

export const DownloadButtonsWrapper = styled.div`
  display: flex;
  flex-direction: row;
  gap: 0.5em;
  align-items: center;
  justify-content: center;
  /* align-items: center; */
  /* gap: 1em; */
`;
export const RetryButton = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;
  min-width: 30%;
  min-height: 110%;
  background-color: #A9907E;
  color: white;
  /* font-size: 1.1em; */
  padding: 1em;
  border: none;
  border-radius: 1.2em;
  margin-bottom: 0.1em;
  cursor: pointer;
  /* margin-top: 1em; */
  box-shadow: 0 10px 12px rgba(0, 0, 0, 0.3);

  &:hover, &:focus {
    background-color: #BFB29E;
  }
`;

export const RetryIcon = styled(VscRefresh)`
    width: 20px;
    height: 20px;
`;