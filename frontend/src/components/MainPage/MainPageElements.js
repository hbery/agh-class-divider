import styled from 'styled-components';

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
  width: 50em;
  margin-bottom: 20px;
  gap: 3em;
  padding: 1em;
`;

export const SelectFileTitle = styled.p`
  width: 60%;
  text-align: center;
`;

export const SelectScheduleWrapper = styled.div`
display: flex;
flex-direction: column;
justify-content: center;
align-items: center;
border: solid 1px pink;
background-color: #ABC4AA;
padding: 1em;
border-radius: 1.2em;
border: 1px #698269 solid;
width: 12em;
height: 18em;
`;

export const SelectGroupWrapper = styled.div`
display: flex;
justify-content: center;
align-items: center;
flex-direction: column;
background-color: #ABC4AA;
padding: 1em;
border-radius: 1.2em;
border: 1px #698269 solid;
width: 12em;
height: 18em;
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
  padding: 10px;
  border: none;
  border-radius: 1.2em;
  cursor: pointer;

  &:hover, &:focus {
        background-color: #BFB29E;
    }
`;

export const ConfirmButtonWrapper = styled.div`
  margin-top: 20px;
`;

export const ConfirmButton = styled.button`
  background-color: #86a660;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 1.2em;
  cursor: pointer;

  &:hover, &:focus {
        background-color: #a4b888;
    }
`;

