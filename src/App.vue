<template>
  <div id="app">
    <h1>Granular Pad Sound Composer</h1>
    <input type="file" @change="onFileChange" accept="audio/*" />
    <input type="range" min="0" max="1" step="0.1" v-model="randomnessLevel" />
    <button @click="convertToMIDI">Generate Composition</button>
    <div>
      <a :href="midiFile ? midiFile : '#'" download="generated_output.mid">
        <button @click="checkDownload">Download MIDI</button>
      </a>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      randomnessLevel: 0.5,
      midiFile: null,
    };
  },
  methods: {
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    async convertToMIDI() {
      if (!this.selectedFile) {
        alert("Please select an audio file first.");
        return;
      }

      const formData = new FormData();
      formData.append("file", this.selectedFile);
      formData.append("randomness", this.randomnessLevel);

      try {
        const response = await fetch("http://localhost:5000/upload", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          const blob = await response.blob();
          this.midiFile = URL.createObjectURL(blob);
        } else {
          this.midiFile = null;
          alert("Failed to generate composition. Please try again.");
        }
      } catch (error) {
        this.midiFile = null;
        console.error("Error:", error);
        alert("An error occurred while generating the composition.");
      }
    },
    checkDownload() {
      if (!this.midiFile) {
        alert(
          "No MIDI file available for download. Please try generating again."
        );
      }
    },
  },
};
</script>

<style scoped>
#app {
  text-align: center;
  margin-top: 50px;
}
button,
input[type="range"] {
  margin-top: 20px;
}
a {
  display: block;
  margin-top: 20px;
}
</style>
