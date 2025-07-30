import config from '../config';
const MainContent = () => {
    return (
        <div className="main-content">
            <h1 style={{ color: 'red' }}>About Kmart</h1>
            <img src={config.building1} style={{ margin: '0 auto' }} alt="Kmart Building" />
            <div className="home-text">
            <p>Want to know about what goes on inside VRC Kmart?</p> 
            <p> Explore behind the scenes of your favorite retailer in Virtual Reality.</p> 
            <p>Read below for an insight as to where you want to click next.</p>
            </div>
            <div className="home-story">

            <button style={{ color: 'red', border: 'none', outline: 'none', textDecoration: 'underline' }}>The VRC Kmart Story</button>
            <p>The story of a search for nostalgia and community, <br></br>learn how we brought Kmart into the virtual world.</p>
            <button style={{ color: 'red', border: 'none', outline: 'none', textDecoration: 'underline' }}>VRC Kmart Officers</button>
            <p>See VRC Kmart's officers that help run this group.</p>
            <button style={{ color: 'red', border: 'none', outline: 'none', textDecoration: 'underline' }}>1996 Kmart Officers</button>
            <p>See Kmart's officers from 1996, the time this website was based from.</p>
            <button style={{ color: 'red', border: 'none', outline: 'none', textDecoration: 'underline' }}>Kmart Facts</button>
            <p>A year-by-year listing of Kmart's real-life and virtual milestones.</p>
            <button style={{ color: 'red', border: 'none', outline: 'none', textDecoration: 'underline' }}>Kmart Fun Facts</button>
            <p>Amaze your friends with your awesome knowledge of Kmart!</p>
            <button style={{ color: 'red', border: 'none', outline: 'none', textDecoration: 'underline' }}>Kmart Financials</button>
            <p>VRC Kmart Corporation's financial performance, history and background info.</p>
            <button style={{ color: 'red', border: 'none', outline: 'none', textDecoration: 'underline' }}>Kmart History</button>
            <p>Straight from the Sears Archive, the rise of Kmart to becoming America's Favorite Store.</p>
           </div>
        </div>
    );
}

export default MainContent;