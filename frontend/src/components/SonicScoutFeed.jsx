import { useState, useEffect, useRef } from "react";

const MOCK_TRACKS = [
  {
    id: 1,
    title: "Hyperspace",
    artist: "Avalon Emerson",
    genre: "Breakbeat Techno",
    genreColor: "#00e5a0",
    bpm: 138,
    year: 2024,
    label: "AD 93",
    artwork: null,
    aiContext: {
      genreDescription: "Breakbeat techno fuses the syncopated, chopped-up drum patterns of breakbeat with the relentless drive of techno. It emerged in the early 2010s as producers started reintroducing breakbeats into warehouse techno sets, reacting against the dominance of four-to-the-floor.",
      funFact: "Avalon Emerson started DJing at house parties in Tucson, Arizona before relocating to Berlin. She's known for blending rave nostalgia with experimental sound design.",
      relatedGenres: ["Electro", "IDM", "UK Hardcore"],
      keyArtists: ["Shanti Celeste", "Call Super", "Peach"],
      sceneOrigin: "Berlin / San Francisco crossover, 2014–present",
    },
  },
  {
    id: 2,
    title: "Stasis Field",
    artist: "Objekt",
    genre: "Deconstructed Club",
    genreColor: "#a78bfa",
    bpm: 145,
    year: 2023,
    label: "PAN",
    artwork: null,
    aiContext: {
      genreDescription: "Deconstructed club takes the building blocks of dance music — kicks, snares, synth stabs — and reassembles them into fractured, unpredictable structures. It intentionally subverts expectations of when the drop comes or if it comes at all.",
      funFact: "Objekt (TJ Hertz) has a degree in Acoustic Engineering from the University of Edinburgh and builds custom Max/MSP patches for his live performances.",
      relatedGenres: ["Experimental Bass", "Post-Dubstep", "Footwork"],
      keyArtists: ["Arca", "SOPHIE", "Lotic"],
      sceneOrigin: "Online / Berlin / London triangle, 2015–present",
    },
  },
  {
    id: 3,
    title: "Midnight Protocol",
    artist: "Dopplereffekt",
    genre: "Electro",
    genreColor: "#38bdf8",
    bpm: 128,
    year: 2022,
    label: "Leisure System",
    artwork: null,
    aiContext: {
      genreDescription: "Electro (not to be confused with electro house) is rooted in the machine funk of the early 1980s — 808 drum machines, vocoder vocals, and synthesized basslines. It's the direct descendant of Kraftwerk's electronic futurism filtered through Detroit and New York.",
      funFact: "Dopplereffekt is one of the most mysterious acts in electronic music. The duo has never given a face-to-camera interview and all press photos are obscured or distorted.",
      relatedGenres: ["Detroit Techno", "Miami Bass", "Synthwave"],
      keyArtists: ["Drexciya", "DJ Stingray", "Helena Hauff"],
      sceneOrigin: "Detroit / Düsseldorf axis, 1982–present",
    },
  },
  {
    id: 4,
    title: "Pressure",
    artist: "Skee Mask",
    genre: "Atmospheric Jungle",
    genreColor: "#f59e0b",
    bpm: 162,
    year: 2023,
    label: "Ilian Tape",
    artwork: null,
    aiContext: {
      genreDescription: "Atmospheric jungle combines the frenetic amen break chopping of 90s jungle with lush ambient pads and deep sub-bass. It's a meditative take on one of dance music's most intense forms — breakneck drums floating in reverb-drenched space.",
      funFact: "Skee Mask (Bryan Müller) from Munich is famously private and rarely performs live. His album 'Compro' is considered one of the defining electronic records of the 2010s.",
      relatedGenres: ["Drum & Bass", "Ambient Techno", "Intelligent DnB"],
      keyArtists: ["Photek", "dBridge", "Burial"],
      sceneOrigin: "Munich / London, revival from 2016–present",
    },
  },
];

function GenreTag({ genre, color }) {
  return (
    <span
      style={{
        display: "inline-block",
        padding: "3px 10px",
        borderRadius: "20px",
        fontSize: "11px",
        fontWeight: 600,
        letterSpacing: "0.05em",
        textTransform: "uppercase",
        color: color,
        border: `1px solid ${color}33`,
        background: `${color}12`,
      }}
    >
      {genre}
    </span>
  );
}

function WaveformViz({ color, bpm }) {
  const bars = 48;
  const seed = bpm * 7;
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: "1.5px",
        height: "32px",
        padding: "0 4px",
        opacity: 0.5,
      }}
    >
      {Array.from({ length: bars }, (_, i) => {
        const h = 6 + Math.abs(Math.sin((seed + i * 0.8) * 0.4)) * 24;
        return (
          <div
            key={i}
            style={{
              width: "2px",
              height: `${h}px`,
              borderRadius: "1px",
              background: color,
              opacity: 0.3 + Math.abs(Math.sin((seed + i) * 0.3)) * 0.7,
            }}
          />
        );
      })}
    </div>
  );
}

function RelatedTag({ label }) {
  return (
    <span
      style={{
        display: "inline-block",
        padding: "3px 8px",
        borderRadius: "4px",
        fontSize: "11px",
        color: "#a1a1aa",
        background: "#27272a",
        border: "1px solid #3f3f46",
      }}
    >
      {label}
    </span>
  );
}

function TrackCard({ track, isExpanded, onToggle }) {
  const { title, artist, genre, genreColor, bpm, year, label, aiContext } =
    track;

  return (
    <div
      style={{
        background: "#18181b",
        borderRadius: "12px",
        border: `1px solid ${isExpanded ? genreColor + "40" : "#27272a"}`,
        overflow: "hidden",
        transition: "border-color 0.3s ease",
      }}
    >
      {/* Main card content */}
      <div
        style={{ padding: "20px", cursor: "pointer" }}
        onClick={onToggle}
      >
        {/* Top row: artwork placeholder + track info */}
        <div style={{ display: "flex", gap: "16px", alignItems: "flex-start" }}>
          {/* Artwork placeholder */}
          <div
            style={{
              width: "72px",
              height: "72px",
              minWidth: "72px",
              borderRadius: "8px",
              background: `linear-gradient(135deg, ${genreColor}22, ${genreColor}08)`,
              border: `1px solid ${genreColor}20`,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
              <circle
                cx="12"
                cy="12"
                r="10"
                stroke={genreColor}
                strokeWidth="1"
                opacity="0.4"
              />
              <circle
                cx="12"
                cy="12"
                r="4"
                stroke={genreColor}
                strokeWidth="1"
                opacity="0.6"
              />
              <circle cx="12" cy="12" r="1.5" fill={genreColor} opacity="0.8" />
            </svg>
          </div>

          {/* Track info */}
          <div style={{ flex: 1, minWidth: 0 }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                marginBottom: "4px",
                flexWrap: "wrap",
              }}
            >
              <h3
                style={{
                  margin: 0,
                  fontSize: "17px",
                  fontWeight: 600,
                  color: "#fafafa",
                  letterSpacing: "-0.01em",
                }}
              >
                {title}
              </h3>
              <GenreTag genre={genre} color={genreColor} />
            </div>
            <p
              style={{
                margin: "2px 0 0",
                fontSize: "14px",
                color: "#a1a1aa",
              }}
            >
              {artist}
              <span style={{ color: "#52525b", margin: "0 6px" }}>/</span>
              {label}
              <span style={{ color: "#52525b", margin: "0 6px" }}>/</span>
              {year}
            </p>
          </div>

          {/* BPM badge */}
          <div
            style={{
              padding: "4px 10px",
              borderRadius: "6px",
              background: "#27272a",
              fontSize: "12px",
              color: "#71717a",
              fontVariantNumeric: "tabular-nums",
              whiteSpace: "nowrap",
            }}
          >
            {bpm} BPM
          </div>
        </div>

        {/* Waveform */}
        <div style={{ marginTop: "12px" }}>
          <WaveformViz color={genreColor} bpm={bpm} />
        </div>

        {/* Expand hint */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            marginTop: "8px",
          }}
        >
          <svg
            width="16"
            height="16"
            viewBox="0 0 16 16"
            style={{
              transform: isExpanded ? "rotate(180deg)" : "rotate(0deg)",
              transition: "transform 0.3s ease",
              opacity: 0.3,
            }}
          >
            <path
              d="M4 6L8 10L12 6"
              stroke="#a1a1aa"
              strokeWidth="1.5"
              fill="none"
              strokeLinecap="round"
            />
          </svg>
        </div>
      </div>

      {/* AI Context Panel (expandable) */}
      {isExpanded && (
        <div
          style={{
            borderTop: `1px solid ${genreColor}20`,
            background: `linear-gradient(180deg, ${genreColor}06, transparent)`,
          }}
        >
          {/* Genre explainer */}
          <div style={{ padding: "20px 20px 0" }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "6px",
                marginBottom: "8px",
              }}
            >
              <svg width="14" height="14" viewBox="0 0 16 16" fill={genreColor} opacity="0.6">
                <path d="M8 1a7 7 0 100 14A7 7 0 008 1zm-.5 3.5a.75.75 0 011.5 0v.5a.75.75 0 01-1.5 0v-.5zm-.25 3h1.5v4h-1.5v-4z" />
              </svg>
              <span
                style={{
                  fontSize: "11px",
                  fontWeight: 600,
                  textTransform: "uppercase",
                  letterSpacing: "0.08em",
                  color: genreColor,
                  opacity: 0.8,
                }}
              >
                Genre context
              </span>
            </div>
            <p
              style={{
                margin: 0,
                fontSize: "13.5px",
                lineHeight: 1.65,
                color: "#d4d4d8",
              }}
            >
              {aiContext.genreDescription}
            </p>
            <p
              style={{
                margin: "6px 0 0",
                fontSize: "12px",
                color: "#71717a",
              }}
            >
              Scene: {aiContext.sceneOrigin}
            </p>
          </div>

          {/* Fun fact */}
          <div style={{ padding: "16px 20px 0" }}>
            <div
              style={{
                padding: "12px 16px",
                borderRadius: "8px",
                background: "#27272a",
                border: "1px solid #3f3f46",
              }}
            >
              <span
                style={{
                  fontSize: "11px",
                  fontWeight: 600,
                  textTransform: "uppercase",
                  letterSpacing: "0.08em",
                  color: "#a1a1aa",
                  display: "block",
                  marginBottom: "4px",
                }}
              >
                Fun fact
              </span>
              <p
                style={{
                  margin: 0,
                  fontSize: "13px",
                  lineHeight: 1.6,
                  color: "#d4d4d8",
                }}
              >
                {aiContext.funFact}
              </p>
            </div>
          </div>

          {/* Related genres + key artists */}
          <div style={{ padding: "16px 20px 20px" }}>
            <div style={{ marginBottom: "12px" }}>
              <span
                style={{
                  fontSize: "11px",
                  fontWeight: 600,
                  textTransform: "uppercase",
                  letterSpacing: "0.08em",
                  color: "#71717a",
                  display: "block",
                  marginBottom: "6px",
                }}
              >
                Related genres
              </span>
              <div style={{ display: "flex", gap: "6px", flexWrap: "wrap" }}>
                {aiContext.relatedGenres.map((g) => (
                  <RelatedTag key={g} label={g} />
                ))}
              </div>
            </div>
            <div>
              <span
                style={{
                  fontSize: "11px",
                  fontWeight: 600,
                  textTransform: "uppercase",
                  letterSpacing: "0.08em",
                  color: "#71717a",
                  display: "block",
                  marginBottom: "6px",
                }}
              >
                Key artists to explore
              </span>
              <div style={{ display: "flex", gap: "6px", flexWrap: "wrap" }}>
                {aiContext.keyArtists.map((a) => (
                  <RelatedTag key={a} label={a} />
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function SonicScoutFeed() {
  const [expandedId, setExpandedId] = useState(1);
  const [filter, setFilter] = useState("all");

  const genres = [...new Set(MOCK_TRACKS.map((t) => t.genre))];
  const filtered =
    filter === "all" ? MOCK_TRACKS : MOCK_TRACKS.filter((t) => t.genre === filter);

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#09090b",
        color: "#fafafa",
        fontFamily:
          '"SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: "24px 20px 16px",
          borderBottom: "1px solid #1c1c1e",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <div>
            <h1
              style={{
                margin: 0,
                fontSize: "22px",
                fontWeight: 700,
                letterSpacing: "-0.03em",
                background: "linear-gradient(135deg, #fafafa, #71717a)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              SonicScout
            </h1>
            <p
              style={{
                margin: "2px 0 0",
                fontSize: "12px",
                color: "#52525b",
                letterSpacing: "0.04em",
              }}
            >
              Discover · Understand · Explore
            </p>
          </div>
          <div
            style={{
              width: "32px",
              height: "32px",
              borderRadius: "50%",
              background: "#27272a",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: "pointer",
            }}
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="#71717a">
              <circle cx="8" cy="3" r="1.5" />
              <circle cx="8" cy="8" r="1.5" />
              <circle cx="8" cy="13" r="1.5" />
            </svg>
          </div>
        </div>

        {/* Genre filter pills */}
        <div
          style={{
            display: "flex",
            gap: "6px",
            marginTop: "14px",
            overflowX: "auto",
            paddingBottom: "2px",
          }}
        >
          <button
            onClick={() => setFilter("all")}
            style={{
              padding: "5px 14px",
              borderRadius: "20px",
              border: "1px solid",
              borderColor: filter === "all" ? "#fafafa" : "#3f3f46",
              background: filter === "all" ? "#fafafa" : "transparent",
              color: filter === "all" ? "#09090b" : "#a1a1aa",
              fontSize: "12px",
              fontWeight: 500,
              cursor: "pointer",
              whiteSpace: "nowrap",
              transition: "all 0.2s",
            }}
          >
            All
          </button>
          {genres.map((g) => {
            const c = MOCK_TRACKS.find((t) => t.genre === g)?.genreColor;
            const active = filter === g;
            return (
              <button
                key={g}
                onClick={() => setFilter(g)}
                style={{
                  padding: "5px 14px",
                  borderRadius: "20px",
                  border: "1px solid",
                  borderColor: active ? c : "#3f3f46",
                  background: active ? `${c}20` : "transparent",
                  color: active ? c : "#a1a1aa",
                  fontSize: "12px",
                  fontWeight: 500,
                  cursor: "pointer",
                  whiteSpace: "nowrap",
                  transition: "all 0.2s",
                }}
              >
                {g}
              </button>
            );
          })}
        </div>
      </div>

      {/* Feed */}
      <div style={{ padding: "16px 16px 40px", display: "flex", flexDirection: "column", gap: "12px" }}>
        {filtered.map((track) => (
          <TrackCard
            key={track.id}
            track={track}
            isExpanded={expandedId === track.id}
            onToggle={() =>
              setExpandedId(expandedId === track.id ? null : track.id)
            }
          />
        ))}
      </div>

      {/* Bottom status bar */}
      <div
        style={{
          position: "sticky",
          bottom: 0,
          padding: "12px 20px",
          background: "linear-gradient(transparent, #09090b 40%)",
          display: "flex",
          justifyContent: "center",
        }}
      >
        <span
          style={{
            fontSize: "11px",
            color: "#3f3f46",
            letterSpacing: "0.06em",
            textTransform: "uppercase",
          }}
        >
          {filtered.length} tracks · AI context powered by RAG + Claude
        </span>
      </div>
    </div>
  );
}
